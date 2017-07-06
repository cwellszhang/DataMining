# coding=utf-8
## Spark Application - execute with spark-submit
#  FP-growth model
## Imports
from pyspark import SparkConf, SparkContext
from pyspark.mllib.fpm import FPGrowth
from pyspark.mllib.fpm import FPGrowthModel

## Module Constants
APP_NAME = "FP-growth Application"
## Main functionality
def main(sc):
     # Load the  data
     dataNode = sc.textFile("Groceries.txt")
     # filter the data
     dataNode= dataNode.filter(lambda x:True if "items" not in x else False)
     # print dataNode.take(5)
     # get necessary column
     dataBad = dataNode.map(lambda x:x.split("{"))
     dataGood = dataBad.map(lambda x:x[1].replace("}\"",""))
     fpData = dataGood.map(lambda x:x.split(",")).cache()
     model = FPGrowth.train(fpData,0.05,3)
     for i in  sorted(model.freqItemsets().collect()):
         print i.items,i.freq,'\n'

     # save model
     # model_path =  "./fpm"
     # model.save(sc, model_path)
     # sameModel = FPGrowthModel.load(sc, model_path)

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    # Execute Main functionality
    main(sc)
