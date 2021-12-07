import time
import datetime
import threading
import numpy as np
import pandas as pd
import uuid
import random
from collections import defaultdict
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


class LOB:
    def __init__(self):
        self.order_count = 0
        self.order_book = {}
        self.offer_queue = []
        self.bid_queue = []
        self.logs = []
        self.period_counter = 1
        self.order_volume = {}
        self.trade_volume = {} # match
        self.bid_volume = {}
        self.ask_volume = {}
        self._running = True

    def create_order_id(self):
        self.order_count += 1
        return self.order_count

    @property
    def best_bid_offer(self):
        best = {}
        if len(self.bid_queue):
            best['bid'] = self.order_book[self.bid_queue[-1]]["price"]
        if len(self.offer_queue):
            best['ask'] = self.order_book[self.offer_queue[0]]["price"]
        return best


    def add_to_queue(self, action, order_id, order):
        if action == "ask":
            queue = self.offer_queue
            try:
                self.ask_volume[self.period_counter] += 1
            except:
                pass
        elif action == "bid":
            queue = self.bid_queue
            try:
                self.bid_volume[self.period_counter] += 1
            except:
                pass
        if not queue:
            queue.append(order_id)
        else:
            i = len(queue) - 1
            queue.append(0)
            while i >= 0 and self.order_book[queue[i]]["price"] > order["price"]:
                queue[i + 1] = queue[i]
                i -= 1
            queue[i + 1] = order_id


    def create_limit_order(self, action, user_id, quantity, price):
        order_id = self.create_order_id()
        order = {
            "action": action,
            "order_id": order_id,
            "user_id": user_id,
            "quantity": quantity,
            "price": price,
            "timestamp": str(datetime.datetime.now())
            }
        self.order_book[order_id] = order
        if action == "ask" or action == "bid":
            self.add_to_queue(action, order_id, order)
        else:
            print("ERROR! Wrong action.")
        self.settle()


    def cancel_limit_order(self, order_id):
        if self.order_book[order_id]["action"] == 'ask':
            for i in range(len(self.offer_queue)):
                if self.offer_queue[i] == order_id:
                    del self.offer_queue[i]
                    break
        else:
            for i in range(len(self.bid_queue)):
                if self.bid_queue[i] == order_id:
                    del self.bid_queue[i]
                    break
        del self.order_book[order_id]


    def create_market_order(self, action, quantity):
        stock_count = 0
        stock_price = 0
        if action == "bid":
            i = len(self.bid_queue) - 1
            while quantity != 0 and i >= 0:
                id = self.bid_queue[-1]
                temp = self.order_book[id]["quantity"]
                if temp <= quantity:
                    quantity -= temp
                    stock_count += temp
                    stock_price += temp * self.order_book[id]["price"]
                    self.cancel_limit_order(id)
                else:
                    self.order_book[id]["quantity"] -= quantity
                    stock_count += quantity
                    stock_price += quantity * self.order_book[id]["price"]
                    quantity = 0
                i -= 1

        elif action == "ask":
            i = 0
            while quantity != 0 and i < len(self.offer_queue):
                id = self.offer_queue[0]
                temp = self.order_book[id]["quantity"]
                if temp <= quantity:
                    quantity -= temp
                    stock_count += temp
                    stock_price += temp * self.order_book[id]["price"]
                    self.cancel_limit_order(id)
                else:
                    self.order_book[id]["quantity"] -= quantity
                    stock_count += quantity
                    stock_price += quantity * self.order_book[id]["price"]
                    quantity = 0
                i += 1
            try:
                return [stock_count, stock_price / stock_count]
            except:
                print('stock_count: ',stock_count,'stock_price: ',stock_price)
                return [0, 0]


    def settle(self):
        while self.bid_queue and self.offer_queue and self.order_book[self.bid_queue[-1]]["price"] >= self.order_book[self.offer_queue[0]]["price"]:
            order = {}
            if self.order_book[self.bid_queue[-1]]["quantity"] > self.order_book[self.offer_queue[0]]["quantity"]:
                order = self.order_book[self.offer_queue[0]]
                self.cancel_limit_order(self.offer_queue[0]) # remove order from queue
                self.create_market_order('bid', order["quantity"])
                self.trade_volume[self.period_counter] += 1
            elif self.order_book[self.bid_queue[-1]]["quantity"] < self.order_book[self.offer_queue[0]]["quantity"]:
                order = self.order_book[self.bid_queue[-1]]
                self.cancel_limit_order(self.bid_queue[-1])
                self.create_market_order('ask', order["quantity"])
                self.trade_volume[self.period_counter] += 1
            else:
                self.cancel_limit_order(self.offer_queue[0])
                self.cancel_limit_order(self.bid_queue[-1])



def demo():
    lob_example = LOB()
    lob_example.create_limit_order('ask', 'alice', 10, 100)
    view_lob()

    lob_example.create_limit_order('bid', 'charles', 20, 85)
    view_lob()

    lob_example.create_limit_order('ask', 'bob', 5, 110)
    view_lob()


def distributions():
    traders = 1000 # ?
    trader_arrival_rate = 0.2 # mean interval rate
    poisson = random.expovariate(1.0/trader_arrival_rate) #poisson
    expo = np.random.exponential(trader_arrival_rate)
    check_min, check_max = 0.5, 1.0
    uniform_check_time = random.uniform(check_min, check_max) # uniform distribution



def qa_lengths():
    print('periods: ', len(periods)) # expected 10
    print('LOB.logs: ', len(LOB1.logs)) # expected 10
    print('LOB1.order_volume: ', len(LOB1.order_volume)) # expected 10
    print('LOB1.period_counter: ', LOB1.period_counter) # expected 11


def distribution2():
    periods = [i for i in range(1,24)]
    lmbda = 1
    poisson_pd = poisson.pmf(periods, lmbda)
    print(poisson_pd)
    time_period = 1
    for pd in poisson_pd:
        for i in range(1,10000):
            t_i = np.random.choice(2, 1, p=[1-pd, pd])[0]
        time_period += 1



def view_lob():
    print('order_book', lob_example.order_book)
    print('offer_queue', lob_example.offer_queue)
    print('bid_queue', lob_example.bid_queue)
    print('best_bid_offer', lob_example.best_bid_offer)



def _run_simulation(LOB, periods):
    LOB.order_volume = {i:0 for i in range(1, len(periods)+1)}
    LOB.trade_volume = {i:0 for i in range(1, len(periods)+1)}
    LOB.bid_volume = {i:0 for i in range(1, len(periods)+1)}
    LOB.ask_volume = {i:0 for i in range(1, len(periods)+1)}

    while LOB._running and LOB.period_counter <= len(periods):
        counter = LOB.period_counter
        p = periods[counter-1]
        t_i = np.random.choice(2, 1, p=[1-p, p])[0]
        if t_i == 1:
            make_order(LOB)
            LOB.order_volume[counter] += 1



def _logger(LOB, periods, period_sec=5):
    #while LOB._running:
    for period in periods:
        time.sleep(period_sec)
        period_log = {'period':LOB.period_counter, 'order_book':LOB.order_book, 'bbo':LOB.best_bid_offer}
        LOB.logs.append(period_log)
        print(LOB.period_counter, LOB.best_bid_offer)
        LOB.period_counter += 1
        if LOB.period_counter > len(periods):
            LOB._running = False

        # RESET
        LOB.offer_queue = []
        LOB.bid_queue = []
        LOB.order_book = {}



def get_qty_range(full_dfs):
    max_i = 0
    for i in range(len(full_dfs)):
        df_i = full_dfs[i][['order_id','quantity','price']]
        temp_df = df_i.groupby(['price'])['quantity'].sum()
        temp_max = max(temp_df) + int(max(temp_df)*0.05)
        if temp_max > max_i:
            max_i = temp_max
    return [0, max_i]


def get_period_logs(LOB):
    full_dfs = []
    for i in range(len(LOB.logs)):
        dfs = []
        for k,v in LOB.logs[i]['order_book'].items():
            df = pd.DataFrame([v])
            dfs.append(df)
        period_df = pd.concat(dfs)
        period_df['period_i'] = i
        full_dfs.append(period_df)
    #full_dfs = full_dfs[:-1]
    final_df = pd.concat(full_dfs)
    return final_df, full_dfs



def graph_evolution(full_dfs, LOB):
    subplot_titles = ['p{}'.format(i+1) for i in range(len(full_dfs))]
    fig = make_subplots(rows=1, cols=len(full_dfs), specs=[[{} for i in range(len(full_dfs))]], shared_xaxes=True,
                        shared_yaxes=True, vertical_spacing=0.001, x_title='quantity', subplot_titles=subplot_titles)

    qty_range = get_qty_range(full_dfs)
    asks = [i['bbo']['ask'] for i in LOB.logs]
    bids = [i['bbo']['bid'] for i in LOB.logs]

    for i in range(len(full_dfs)):
        df_i = full_dfs[i][['order_id','quantity','price']]
        bar = go.Bar(
            x=list(df_i['quantity']),y=list(df_i['price']),
            marker=dict(color='rgba(50, 171, 96, 0.6)',line=dict(color='rgba(50, 171, 96, 1.0)',width=1)),
            name='p{}'.format(i+1),orientation='h',
        )
        fig.append_trace(bar, 1, i+1)
        fig.append_trace(go.Scatter(x=[df_i['quantity'].mean()],y=[bids[i]],mode="markers+lines",line=dict(color="blue")), 1, i+1)
        fig.append_trace(go.Scatter(x=[df_i['quantity'].mean()],y=[asks[i]],mode="markers+lines",line=dict(color="red")), 1, i+1)
        fig.append_trace(go.Scatter(x=[qty_range[1]],y=[bids[i]],mode="markers+lines",line=dict(color="white")), 1, i+1) # range
        if i == 0:
            fig['layout']['yaxis']['showticklabels'] = False
            fig['layout']['xaxis']['autorange'] = 'reversed'
        elif i == (len(full_dfs)-1):
            fig['layout']['yaxis{}'.format(i+1)]['showticklabels'] = True
            fig['layout']['yaxis{}'.format(i+1)]['side'] = 'right'
            fig['layout']['xaxis{}'.format(i+1)]['autorange'] = 'reversed'
            fig['layout']['yaxis{}'.format(i+1)]['title'] = 'price'
        else:
            fig['layout']['xaxis{}'.format(i+1)]['autorange'] = 'reversed'


    fig.update_layout(title='LOB Over {} Periods'.format(len(periods)), showlegend=False)
    return fig


def plot_trades(LOB):
    bid_pct = ['{}%'.format(round(i[0]/sum(i)*100,2)) for i in zip (LOB.bid_volume.values(), LOB.ask_volume.values())]
    ask_pct = ['{}%'.format(round(i[1]/sum(i)*100,2)) for i in zip (LOB.bid_volume.values(), LOB.ask_volume.values())]
    fig = go.Figure(data=[
        go.Bar(name='bid_volume', x=list(LOB.bid_volume.keys()), y=list(LOB.bid_volume.values()),
              text=bid_pct,textposition='auto',textfont_color="white", marker_color='lightsalmon'),
        go.Bar(name='ask_volume', x=list(LOB.ask_volume.keys()), y=list(LOB.ask_volume.values()),
               text=ask_pct,textposition='auto',textfont_color="white", marker_color='indianred')
    ])

    fig.update_layout(barmode='stack', title_text='Orders by Period - Bids & Asks',
                      yaxis={'title':'volume'}, xaxis={'title':'periods','tickmode':'linear'})
    return fig


def plot_activity(LOB):
    fig = go.Figure(data=[
        go.Bar(name='trade_volume', x=list(LOB.trade_volume.keys()), y=list(LOB.trade_volume.values()), marker_color='lightsalmon'),
        go.Bar(name='order_volume', x=list(LOB.order_volume.keys()), y=list(LOB.order_volume.values()), marker_color='indianred')
    ])

    fig.update_layout(barmode='group', title_text='LOB Activity - Trades & Orders',
                      yaxis={'title':'volume'}, xaxis={'title':'periods','tickmode':'linear'})
    return fig



def run_dash_app():
    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=False)



def make_order(LOB):
    user_id = str(uuid.uuid4())

    price = np.random.normal(100, 10, 1) # (mean, std_dev, num)
    price = int(price[0])

    qty = np.random.normal(80, 10, 1) # (mean, std_dev, num)
    qty = int(qty[0])

    action = np.random.choice(2, 1, p=[0.5, 0.5])[0] # ACTION (bid=0 vs ask=1)
    action = 'bid' if action == 0 else 'ask'

    trade = np.random.choice(2, 1, p=[0.8, 0.2])[0] # TRADE (limit vs market)
    #trade_func = LOB.create_limit_order(action, user_id, price, qty) if trade == 0 else LOB.create_market_order(action, qty)

    LOB.create_limit_order(action, user_id, price, qty)



if __name__=='__main__':
    LOB1 = LOB()

    # poisson distribution (trade frequency)
    periods = [.4,.05,.05,.05,.05,.05,.05,.05,.05,.5]
    period_secs = 4

    # Start Threads
    simulationThread = threading.Thread(target=_run_simulation, kwargs={'LOB':LOB1, 'periods':periods})
    logThread = threading.Thread(target=_logger, kwargs={'LOB':LOB1, 'periods':periods, 'period_sec':period_secs})
    simulationThread.start()
    logThread.start()

    while LOB1._running:
        if LOB1.period_counter <= len(periods):
            continue
        else:
            LOB1._running = False
            #LOB1.terminate()
            break


    final_df, full_dfs = get_period_logs(LOB=LOB1)
    #final_df.head()

    fig = graph_evolution(full_dfs, LOB1)
    pio.write_image(fig, 'images/lob_evolution.png') #fig.show()

    fig2 = plot_trades(LOB1)
    pio.write_image(fig2, 'images/lob_trades.png')

    fig3 = plot_activity(LOB1)
    pio.write_image(fig3, 'images/lob_activity.png')
