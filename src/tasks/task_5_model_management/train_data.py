import mlflow.xgboost
import our_model as omd
from load_dataset import load_dataset

if __name__ == '__main__':
    mlflow.set_experiment('name')
    with mlflow.start_run(run_name='name') as run:
        x_train, x_test, y_train, y_test = load_dataset(
            'our-dataset', ';'
        )
        cls = omd.our_model(some parameters)
        cls.fit(x_train, y_train)
        auc = cls.score(x_test, y_test)
        print("AUC ", auc)
        mlflow.log_metric("auc", auc)

        mlflow.our_model.log_model(cls, "name")
        mlflow.end_run()
