from fastapi import FastAPI
import yfinance as yf
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Query
from pypfopt.exceptions import OptimizationError

from enums import ModelMappingEnum, OptimizationTypeEnum
from exceptions import NoOptimalPortfolioException, SomethingWentWrongException, PredictionNegativeStocksException
from service import CalculatePortfolioService, DataService, TickerService
from utils import add_months

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://portfolio-front-diploma.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/predict/")
async def predict(
        tickers_name: str = "LKOH.ME,SBER.ME,YNDX.ME",
        date_from: str = "2020-01-01",
        date_to: str = "2022-05-01",
        total_sum: int = 1000,
        model_name: str = Query(ModelMappingEnum.arima.model_name, enum=ModelMappingEnum.list()),
        optimization_type: str = Query(OptimizationTypeEnum.sharpe.optimization_type, enum=OptimizationTypeEnum.list()),
        month: int = 5
) -> dict[str, list]:
    # LKOH.ME,SBER.ME,YNDX.ME,GMKN.ME,DSKY.ME,NKNC.ME,MTSS.ME,IRAO.ME,AFLT.ME
    Model = ModelMappingEnum[model_name]
    OptimizationType = OptimizationTypeEnum[optimization_type]
    df_stocks = DataService(
        tickers_name=tickers_name,
        start=date_from,
        end=date_to,
        interval=Model.interval
    ).get_data()
    if Model.need_drop:
        df_stocks = df_stocks.dropna()
    try:
        data_predict = Model.model(data=df_stocks, month=month).get_table_of_predictions()
    except IndexError as e:
        print(e)
        raise SomethingWentWrongException()
    try:
        allocation_shp, rem_shp, pfolio_info = CalculatePortfolioService(data_predict, OptimizationType).calculate(
            total_sum)
    except OptimizationError as e:
        print(e)
        raise NoOptimalPortfolioException()
    except ValueError as e:
        print(e)
        raise PredictionNegativeStocksException()

    tickers_list = tickers_name.split(',')
    labels = list(allocation_shp.keys())
    values = list(map(int, list(allocation_shp.values())))
    others_labels = list(set(tickers_list) - set(labels))

    if len(labels) <= 0 or len(values) <= 0:
        raise NoOptimalPortfolioException()

    sectors = TickerService(allocation_shp).group_by_sector()

    labels_sector = list(sectors.keys())
    values_sector = list(sectors.values())

    tickers_headers = list(df_stocks.keys())
    x_axis = list(map(lambda d: str(d.date()), df_stocks.index))

    if model_name == ModelMappingEnum.neural_month.model_name:
        next_date = df_stocks.index[-1]
        x_axis_pred = [add_months(next_date, months + 1) for months in data_predict.index]
    else:
        x_axis_pred = list(map(lambda d: str(d.date()), data_predict.index))
    x_annotations = x_axis_pred[0]
    series = []

    for t in tickers_headers:
        series.append({"name": t, "data": df_stocks[t].values.tolist() + data_predict[t].values.tolist()})

    return {
        "labels": labels,
        "values": values,
        "other": rem_shp,
        "other_labels": others_labels,
        "labels_sector": labels_sector,
        "values_sector": values_sector,
        "series_stocks": series,
        "x_annotations_stocks": x_annotations,
        "xaxis_stocks": x_axis + x_axis_pred,
        "expected_annual_return": pfolio_info[0] if len(pfolio_info) > 0 else None,
        "annual_volatility": pfolio_info[1] if len(pfolio_info) > 1 else None,
        "sharpe_ratio": pfolio_info[2] if len(pfolio_info) > 2 else None,
    }


@app.get("/ticker/{ticker_name}")
async def ticker(ticker_name: str):
    tick = yf.Ticker(ticker_name)
    return tick.info


@app.get("/models/")
async def get_models() -> list[dict]:
    data = []
    for el in ModelMappingEnum.list():
        model = ModelMappingEnum[el]
        data.append({"model_name": model.model_name, "desc": model.desc, "hint": model.hint})
    return data


@app.get("/optimizators/")
async def get_optimizators() -> list[dict]:
    data = []
    for el in OptimizationTypeEnum.list():
        optim = OptimizationTypeEnum[el]
        data.append({"optimization_type": optim.optimization_type, "desc": optim.desc, "hint": optim.hint})
    return data


@app.get("/tickers/")
async def tickers():
    return ['LKOH.ME', 'GMKN.ME', 'DSKY.ME', 'NKNC.ME', 'MTSS.ME', 'IRAO.ME', 'SBER.ME', 'AFLT.ME', 'YNDX.ME']
