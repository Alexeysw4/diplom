from fastapi import FastAPI
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

    try:
        allocation_shp, rem_shp, pfolio_info = CalculatePortfolioService(data_predict, OptimizationType).calculate(
            total_sum)
    except OptimizationError as e:
        print(e)
        raise NoOptimalPortfolioException(data={"series_stocks": series,
                                                "x_annotations_stocks": str(x_annotations),
                                                "xaxis_stocks": list(map(str, x_axis + x_axis_pred))})
    except ValueError as e:
        print(e)
        raise PredictionNegativeStocksException({"series_stocks": series,
                                                 "x_annotations_stocks": x_annotations,
                                                 "xaxis_stocks": list(map(str, x_axis + x_axis_pred))})

    tickers_list = tickers_name.split(',')
    labels = list(allocation_shp.keys())
    values = list(map(int, list(allocation_shp.values())))
    others_labels = list(set(tickers_list) - set(labels))

    if len(labels) <= 0 or len(values) <= 0:
        raise NoOptimalPortfolioException({"series_stocks": series,
                                           "x_annotations_stocks": x_annotations,
                                           "xaxis_stocks": x_axis + x_axis_pred})

    sectors = TickerService(allocation_shp).group_by_sector()

    labels_sector = list(sectors.keys())
    values_sector = list(sectors.values())

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
    return ['GAZP.ME', 'SBER.ME', 'GMKN.ME', 'LKOH.ME', 'YNDX.ME', 'NVTK.ME', 'ALRS.ME', 'PLZL.ME', 'ROSN.ME',
            'PIKK.ME', 'CHMF.ME', 'MGNT.ME', 'TRNFP.ME', 'TCSG.ME', 'TATN.ME', 'MTSS.ME', 'AFKS.ME',
            'IRAO.ME', 'SBERP.ME', 'VTBR.ME', 'PHOR.ME', 'UPRO.ME', 'RASP.ME', 'NLMK.ME', 'MAGN.ME', 'CBOM.ME',
            'SIBN.ME', 'SNGS.ME', 'MTLR.ME', 'POLY.ME', 'MOEX.ME', 'SNGSP.ME', 'SELG.ME', 'RUAL.ME', 'FIVE.ME',
            'OGKB.ME', 'FESH.ME', 'MTLRP.ME', 'TATNP.ME', 'AFLT.ME', 'AGRO.ME', 'FEES.ME',
            'HYDR.ME', 'ENRU.ME', 'ENPG.ME', 'BANEP.ME', 'AKRN.ME', 'LSNGP.ME', 'LSRG.ME',
            'IRKT.ME', 'RSTI.ME', 'ORUP.ME', 'DSKY.ME', 'RTKM.ME', 'QIWI.ME',
            'VSMO.ME', 'MRKP.ME', 'MSNG.ME', 'BELU.ME', 'FLOT.ME', 'TGKA.ME', 'MVID.ME',
            'MRKK.ME', 'KZOSP.ME', 'ETLN.ME', 'RNFT.ME', 'SPBE.ME', 'BSPB.ME', 'TRMK.ME', 'AQUA.ME',
            'NKNCP.ME', 'BANE.ME', 'NMTP.ME', 'TGKB.ME', 'TGKBP.ME', 'MRKC.ME', 'GCHE.ME', 'UWGN.ME', 'INGR.ME',
            'UNAC.ME', 'DASB.ME', 'KRKNP.ME', 'RTKMP.ME', 'MRKU.ME', 'ISKJ.ME',
            'MRKV.ME', 'RUGR.ME', 'TGKD.ME', 'LNZLP.ME', 'LNZL.ME', 'KAZT.ME', 'MSRS.ME', 'NKSH.ME',
            'AMEZ.ME', 'SFIN.ME', 'KMAZ.ME', 'LIFE.ME', 'GRNT.ME', 'KZOS.ME', 'LSNG.ME', 'NKHP.ME',
            'YAKG.ME', 'ABRD.ME', 'CNTLP.ME', 'RZSB.ME', 'LENT.ME', 'BLNG.ME', 'KUBE.ME', 'NKNC.ME', 'UNKL.ME',
            'RSTIP.ME', 'ROLO.ME', 'DVEC.ME', 'TTLK.ME', 'DIOD.ME', 'MRKZ.ME', 'MGTSP.ME', 'PMSB.ME', 'KAZTP.ME',
            'CNTL.ME', 'STSBP.ME', 'KOGK.ME', 'KRSB.ME', 'APTK.ME', 'NSVZ.ME', 'UTAR.ME', 'MISBP.ME', 'MRKY.ME',
            'LPSB.ME', 'VRSBP.ME', 'KROTP.ME', 'VLHZ.ME', 'ROSB.ME', 'MGNZ.ME', 'GEMA.ME', 'PMSBP.ME', 'SVAV.ME',
            'CHMK.ME', 'MRKS.ME', 'VRSB.ME', 'MRSB.ME', 'IGST.ME', 'KLSB.ME', 'GTRK.ME', 'IGSTP.ME', 'BISVP.ME',
            'ZILL.ME', 'JNOS.ME', 'SIBG.ME', 'PRFN.ME', 'RUSI.ME', 'ZVEZ.ME', 'NNSBP.ME', 'KBSB.ME',
            'KROT.ME', 'USBN.ME', 'NNSB.ME', 'RKKE.ME', 'TGKN.ME', 'KUZB.ME', 'RGSS.ME', 'VJGZ.ME', 'UCSS.ME',
            'VJGZP.ME', 'TGKDP.ME', 'SARE.ME', 'RTGZ.ME', 'RBCM.ME', 'UKUZ.ME', 'BRZL.ME', 'HIMCP.ME',
            'MAGE.ME', 'SAGO.ME', 'SAGOP.ME', 'MAGEP.ME', 'YRSB.ME', 'WTCMP.ME', 'KRSBP.ME', 'MSTT.ME',
            'PAZA.ME', 'NFAZ.ME', 'CHGZ.ME', 'KGKC.ME', 'ELTZ.ME', 'JNOSP.ME', 'YRSBP.ME', 'KRKOP.ME', 'NAUK.ME',
            'KCHE.ME', 'ROST.ME', 'IDVP.ME', 'VSYD.ME', 'STSB.ME', 'VGSBP.ME', 'MFGS.ME', 'ASSB.ME', 'URKZ.ME',
            'KTSB.ME', 'GAZAP.ME', 'PRMB.ME', 'WTCM.ME', 'MISB.ME', 'CHKZ.ME', 'MGTS.ME', 'OMZZP.ME',
            'LVHK.ME', 'VGSB.ME', 'RTSB.ME', 'MFGSP.ME', 'VSYDP.ME', 'TASBP.ME', 'KCHEP.ME', 'RTSBP.ME', 'DZRDP.ME',
            'KRKN.ME', 'ARSA.ME', 'AVAN.ME', 'RDRB.ME', 'TNSE.ME', 'TUZA.ME', 'TORS.ME', 'YKENP.ME',
            'GAZA.ME', 'EELT.ME', 'TASB.ME', 'YKEN.ME', 'MERF.ME', 'ODVA.ME', 'TORSP.ME', 'KMEZ.ME', 'KTSBP.ME',
            'SAREP.ME', 'DZRD.ME', 'KGKCP.ME', 'ACKO.ME', 'BISV.ME', 'GAZT.ME',
            'IRGZ.ME', 'RAVN.ME', 'RUSP.ME', 'TRCN.ME']
