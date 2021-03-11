# 1.sess.run()
# 2.interativesession
# 3.eval(session=sess)

import tensorflow as tf
x = [1,2,3]
W = tf.Variable([0.3], tf.float32)
B = tf.Variable([1.0], tf.float32)

hypothesis = W *x + B

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
aaa = sess.run(hypothesis)
print('aaa : ', aaa)
sess.close()


sess = tf.compat.v1.InteractiveSession()
sess.run(tf.compat.v1.global_variables_initializer())
bbb = hypothesis.eval() # 변수.eval
print('bbb : ',bbb)
sess.close()


sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
ccc = hypothesis.eval(session=sess)
print('ccc : ', ccc)
sess.close()