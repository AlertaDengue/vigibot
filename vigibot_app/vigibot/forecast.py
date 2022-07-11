import os
import pickle

import joblib
from infodenguepredict.data.infodengue import (  # get_city_names
    get_cluster_data,
)
from infodenguepredict.models.quantile_forest import (  # build_model,; calculate_metrics, # noqa
    build_lagged_features,
)
from infodenguepredict.predict_settings import (
    DATA_TYPES,
    PREDICTORS,
    RESULT_PATH,
)


def qf_prediction(city, state, horizon, lookback, doenca="chik"):
    with open("../analysis/clusters_{}.pkl".format(state), "rb") as fp:
        clusters = pickle.load(fp)
    data, group = get_cluster_data(
        city,
        clusters=clusters,
        data_types=DATA_TYPES,
        cols=PREDICTORS,
        doenca=doenca,
    )

    target = "casos_est_{}".format(city)
    casos_est_columns = ["casos_est_{}".format(i) for i in group]
    # casos_columns = ['casos_{}'.format(i) for i in group]

    # data = data_full.drop(casos_columns, axis=1)
    data_lag = build_lagged_features(data, lookback)
    data_lag.dropna()
    data_lag = data_lag["2016-01-01":]
    targets = {}
    for d in range(1, horizon + 1):
        if d == 1:
            targets[d] = data_lag[target].shift(-(d - 1))
        else:
            targets[d] = data_lag[target].shift(-(d - 1))[: -(d - 1)]

    X_data = data_lag.drop(casos_est_columns, axis=1)

    # city_name = get_city_names([city, 0])[0][1]

    #  Load dengue model
    model = joblib.load(
        os.path.join(
            [
                RESULT_PATH,
                "{}/{}_city_model_{}W.joblib".format(state, city, horizon),
            ]
        )
    )
    pred25 = model.predict(X_data, quantile=2.5)
    pred = model.predict(X_data, quantile=50)
    pred975 = model.predict(X_data, quantile=97.5)

    # metrics.to_pickle('{}/{}/qf_metrics_{}.pkl'.format(
    # 'saved_models/quantile_forest', state, city))

    return model, pred, pred25, pred975, X_data, targets, data_lag
