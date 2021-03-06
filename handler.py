import tensorflow as tf
import sys
import json


from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")

def index():
  # change this as you see fit
  #image_path = 'thunder.jpg'
  image_path = request.args.get('image')

  # Read in the image_data
  image_data = tf.gfile.FastGFile('test_images/'+image_path, 'rb').read()

  # Loads label file, strips off carriage return
  label_lines = [line.rstrip() for line
                     in tf.gfile.GFile("models/wildfires/retrained_labels.txt")]

  # Unpersists graph from file
  with tf.gfile.FastGFile("models/wildfires/retrained_graph.pb", 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

  with tf.Session() as sess:
      # Feed the image_data as input to the graph and get first prediction
      softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

      predictions = sess.run(softmax_tensor, \
               {'DecodeJpeg/contents:0': image_data})

      # Sort to show labels of first prediction in order of confidence
      top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
      result = []
      for node_id in top_k:
          human_string = label_lines[node_id]
          score = predictions[0][node_id]
          result.append('%s:%.5f' % (human_string, score))
      return json.dumps(result)

@app.route('/flossy')
def flossy():
    # change this as you see fit
  #image_path = 'thunder.jpg'
  image_path = request.args.get('image')

  # Read in the image_data
  image_data = tf.gfile.FastGFile('test_images/'+image_path, 'rb').read()

  # Loads label file, strips off carriage return
  label_lines = [line.rstrip() for line
                     in tf.gfile.GFile("models/flossy/retrained_labels.txt")]

  # Unpersists graph from file
  with tf.gfile.FastGFile("models/flossy/retrained_graph.pb", 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

  with tf.Session() as sess:
      # Feed the image_data as input to the graph and get first prediction
      softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

      predictions = sess.run(softmax_tensor, \
               {'DecodeJpeg/contents:0': image_data})

      # Sort to show labels of first prediction in order of confidence
      top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
      result = []
      for node_id in top_k:
          human_string = label_lines[node_id]
          score = predictions[0][node_id]
          result.append('%s:%.5f' % (human_string, score))
      return json.dumps(result)

@app.route("/heartbeat")
def heartbeat():
  return "Heart beats ;)"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
