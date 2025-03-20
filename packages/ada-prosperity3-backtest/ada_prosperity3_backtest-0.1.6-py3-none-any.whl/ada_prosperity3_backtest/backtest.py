from .datamodel import *
from .logic import step
from .df_to_states import states_to_df, df_to_states
import os, io, hashlib, contextlib, inspect, warnings
from datetime import datetime
from copy import deepcopy
import pandas as pd
from .log_to_states import read_log
from tqdm import tqdm

class SaveConfig:
    def __init__(self, script=None, infix='', save_dir='ada_backtest'):
        self.script = script
        self.infix = infix
        self.save_dir = save_dir

class BacktestResult:
    def __init__(self, pnls:list[dict[Symbol,int]], sandbox_logs:list[dict], prices_df:pd.DataFrame, trades_df:pd.DataFrame):
        self.pnls = pnls
        self.sandbox_logs = sandbox_logs
        self.prices_df = prices_df
        self.trades_df = trades_df

def get_states_from_log(log_dir) -> list[TradingState]:
    with open(log_dir,'r') as f:
        states = read_log(f.read())
    return states

def get_states_from_round_and_day(round, day) -> list[TradingState]:

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    folder_path = os.path.join(script_dir, "data", f"round{round}", f"day{day}")

    prices_path = os.path.join(folder_path, f"prices{round}{day}.csv")
    trades_path = os.path.join(folder_path, f"trades{round}{day}.csv")

    price_df = pd.read_csv(prices_path, sep=';')
    trade_df = pd.read_csv(trades_path, sep=';')
    states = df_to_states(price_df, trade_df)
    return states


def get_pnl(cash: dict[Symbol, int], state: TradingState):
    pnl = {k:v for k,v in cash.items()}
    for p in state.listings:
        od = state.order_depths[p]
        fair_buy = sum([k*v for k,v in od.buy_orders.items()])/sum(od.buy_orders.values())
        fair_sell = sum([k*v for k,v in od.sell_orders.items()])/sum(od.sell_orders.values())
        fair = (fair_buy+fair_sell)/2
        pnl[p] += fair*state.position.get(p,0)
    return pnl

def save_result(script, output, tag, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    log_folder = os.path.join(save_dir, "log")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    script_folder = os.path.join(save_dir, "script")
    if not os.path.exists(script_folder):
        os.makedirs(script_folder)

    with open(f"{save_dir}/log/{tag}.log","w") as f:
        f.write(output)
    with open(f"{save_dir}/script/{tag}.py","w") as f:
        f.write(script)

# Function to generate the class source code
def generate_class_source(cls):
    # Get the list of functions in the class
    functions = [func for func, _ in inspect.getmembers(cls, predicate=inspect.isfunction)]
    
    # Start the class definition string
    class_code = f"class {cls.__name__}:\n"
    
    # Add each function to the class code
    for func_name in functions:
        func = getattr(cls, func_name)
        # Get the function signature and the function body
        class_code += inspect.getsource(func)

    return class_code

def test_trader_with_states(trader, states: list[TradingState], save_config: SaveConfig):
    if not hasattr(trader, "run"):
        print("Error: The `Trader` class must have a `run` method.")
        return
    if save_config.script is None:
        script = generate_class_source(trader.__class__)
        script = "# WARNING!\n# The back-up class source code is generated dynamically, and is not guaranteed to be correct.\n\n" + script
        warnings.warn("The back-up class source code is generated dynamically, and is not guaranteed to be correct.")
    else:
        script = save_config.script
    n = len(states)
    state = states[0]
    cashes = [{"KELP": 0, "RAINFOREST_RESIN": 0}]
    pnls = [{"KELP": 0, "RAINFOREST_RESIN": 0}]
    sandbox_logs = []
    for i in tqdm(range(n), "Simulation"):
        cash = deepcopy(cashes[-1])
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            orders, conversions, traderData = trader.run(state)
            orders:dict[Symbol, list[Order]]
            conversions: int
            traderData: str
        algo_log = output_buffer.getvalue().strip()
        sandbox_logs.append({
            "sandboxLog": "",
            "lambdaLog": algo_log,
            "timestamp": i*100
        })

        if i<n-1:
            state = step(state, orders, conversions, traderData, states[i+1])
            trades = state.own_trades
            for p in trades:
                for trade in trades[p]:
                    if trade.buyer == "SUBMISSION":
                        cash[p] -= trade.price*trade.quantity
                    if trade.seller == "SUBMISSION":
                        cash[p] += trade.price*trade.quantity
            cashes.append(cash)
            pnls.append(get_pnl(cash, state))
    
    prices_df, trades_df = None, None
    prices_df, trades_df = states_to_df(states, pnls)
    prices_csv = prices_df.to_csv(sep=';', index=False)
    prices_str = io.StringIO(prices_csv).getvalue()
    trades_csv = trades_df.to_csv(sep=';', index=False)
    trades_str = io.StringIO(trades_csv).getvalue()
    
    to_print = "Sandbox logs:\n"+"\n".join([json.dumps(l, indent=2) for l in sandbox_logs])
    to_print += f"\n\n\nActivities log:\n{prices_str}\n\n\nTrade History:\n{trades_str}"
    now = datetime.now()
    hash = hashlib.sha256(script.encode()).hexdigest()[:6]
    tag = now.strftime("%m-%d_%H.%M.%S_") + save_config.infix + hash
    script = f'# Round-Time-Hash Tag: {tag}\n# Final pnls: {pnls[-1]}\n\n'+script
    save_result(script, to_print, tag, save_config.save_dir)
    
    return BacktestResult(
        pnls,
        sandbox_logs,
        prices_df,
        trades_df
    )

def run_backtest_with_round_and_day(trader, round:int, day:int, save_config:SaveConfig=SaveConfig()) -> BacktestResult:
    print(f"Running backtest on day {day} of round {round}")
    states = get_states_from_round_and_day(round, day)
    result = test_trader_with_states(trader, states, SaveConfig(
        save_config.script,
        f'R{round}D{day}_'+save_config.infix,
        save_config.save_dir
    ))
    
    print(f"Round {round} Day {day}", result.pnls[-1], f"Sum {sum(result.pnls[-1].values())}")
    return result

def run_backtest_with_round(trader, round:int, save_config:SaveConfig=SaveConfig()) -> list[BacktestResult]:
    print(f"Running backtest on all days of round {round}")
    days = {
        0: 1
    }
    if round not in days:
        raise NotImplementedError(f"Round {round} not supported yet")
    results = []
    for day in range(days[round]):
        results.append(run_backtest_with_round_and_day(trader, round,day,save_config))
    return results

def run_backtest_with_log(trader, log_dir,save_config=SaveConfig()) -> BacktestResult:
    with open(log_dir,'r') as f:
        states = read_log(f.read())
    result = test_trader_with_states(trader, states, save_config)
    return result