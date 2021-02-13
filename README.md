# MMM---Projekt-zur-Datenanalyse

BertClassifier.ipynb
Die Variable "PATH" muss entsprechend dem aktuellen Dateipfad angepasst werden.

GloveClassifier.ipynb
Die Variable "DATA_PATH" muss entsprechend dem aktuellen Dateipfad angepasst werden.


Die BERT pretrained Models, sowie das GLOVE Model, müssen aus Lea heruntergeladen werden und in die Ordnerstruktur eingebettet werden. (Im Ordner Rezeptklassifikation in Lea)


Die Zellen mit folgendem Code können, sofern nicht Google Colab verwendet wird, ignoriert werden. Falls Google Colab verwendet wird, muss die TPU zuerst in den Einstellungen als Hardware-Beschleuniger eingestellt werden.
	tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
	tf.config.experimental_connect_to_cluster(tpu)
	tf.tpu.experimental.initialize_tpu_system(tpu)
	tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu)

Zellen mit folgendem Code sind nur relevant, falls Keras/Tensorflow so eingestellt ist, dass der Trainingsprozess auf der GPU stattfinden soll.
	config = ConfigProto()
	config.gpu_options.allow_growth = True
	session = InteractiveSession(config=config)


Höchstwahrscheinlich müssen einige Pakete mittels pip install zum erfolgreichen Ausführens des Codes installiert werden. Somit werden die imports zu Beginn Fehler ausgeben.
