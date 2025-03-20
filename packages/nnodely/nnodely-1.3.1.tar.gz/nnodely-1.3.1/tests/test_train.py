import unittest, os, sys
import numpy as np

from nnodely import *
from nnodely.relation import NeuObj
from nnodely.logger import logging, nnLogger

log = nnLogger(__name__, logging.CRITICAL)
log.setAllLevel(logging.CRITICAL)

sys.path.append(os.getcwd())

# 5 Tests
# This file tests the value of the training parameters

data_folder = os.path.join(os.path.dirname(__file__), 'data/')

class ModelyTrainingTest(unittest.TestCase):
    def test_training_values_fir(self):
        NeuObj.clearNames()
        input1 = Input('in1')
        target = Input('out1')
        a = Parameter('a', sw=1, values=[[1]])
        output1 = Output('out', Fir(W=a)(input1.last()))
        output2 = Output('out2', Fir(W_init='init_constant', W_init_params={'value':1})(input1.last()))
        output3 = Output('out3', Fir(W_init='init_exp', b_init='init_exp')(input1.last()))
        output4 = Output('out4', Fir(W_init='init_lin', b_init='init_lin')(input1.last()))
        output5 = Output('out5', Fir(W_init='init_negexp', b_init='init_negexp')(input1.last()))

        test = Modely(visualizer=None,seed=42)
        test.addModel('model', [output1,output2,output3,output4,output5])
        test.addMinimize('error', target.last(), output1)
        test.neuralizeModel()

        dataset = {'in1': [1], 'in2':[[1,2,3]], 'out1': [2]}
        test.loadData(name='dataset', source=dataset)

        self.assertListEqual([[1.0]],test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[3.0]],test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[1.0]],test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=2)
        self.assertListEqual([[1.0]],test.model.all_parameters['a'].data.numpy().tolist())

    def test_training_values_linear(self):
        NeuObj.clearNames()
        input1 = Input('in1')
        input2 = Input('in2', dimensions=3)
        target = Input('out1')
        W = Parameter('W', values=[[1]])
        b = Parameter('b', values=[1])
        output1 = Output('out', Linear(W=W,b=b)(input1.last()))
        output2 = Output('out2', Linear(W_init='init_constant', W_init_params={'value':1})(input1.last()))
        output3 = Output('out3', Linear(W_init='init_exp', b_init='init_exp')(input2.last()))
        output4 = Output('out4', Linear(W_init='init_negexp', b_init='init_negexp')(input2.last()))
        output5 = Output('out5', Linear(W_init='init_lin', b_init='init_lin')(input2.last()))

        test = Modely(visualizer=None, seed=42)
        test.addModel('model', [output1,output2,output3,output4,output5])
        test.addMinimize('error', target.last(), output1)
        test.neuralizeModel()

        dataset = {'in1': [1], 'in2':[[1,2,3]], 'out1': [3]}
        test.loadData(name='dataset', source=dataset)

        self.assertListEqual([[1.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([1.0], test.model.all_parameters['b'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[3.0]], test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([3.0], test.model.all_parameters['b'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[-3.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([-3.0], test.model.all_parameters['b'].data.numpy().tolist())

    def test_training_clear_model(self):
        NeuObj.clearNames()
        input1 = Input('in1')
        target = Input('int1')
        a = Parameter('a', sw=1, values=[[1]])
        fir_out = Fir(W=a)(input1.last())
        output1 = Output('out1', fir_out)

        W = Parameter('W', values=[[1]])
        b = Parameter('b', values=[1])
        output2 = Output('out2', Linear(W=W,b=b)(fir_out))

        test = Modely(visualizer=None, seed=42)
        test.addModel('model', [output1,output2])
        test.addMinimize('error', target.last(), output2)
        test.neuralizeModel()
        self.assertEqual({'out1': [1.0], 'out2': [2.0]}, test({'in1': [1]}))

        dataset = {'in1': [1], 'int1': [3]}
        test.loadData(name='dataset', source=dataset)

        self.assertListEqual([[1.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([1.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[1.0]], test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[3.0]], test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([3.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[3.0]], test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[-51.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([-15.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[-51.0]], test.model.all_parameters['a'].data.numpy().tolist())

        test.neuralizeModel(clear_model=True)
        self.assertListEqual([[1.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([1.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[1.0]], test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[3.0]], test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([3.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[3.0]], test.model.all_parameters['a'].data.numpy().tolist())
        test.trainModel(optimizer='SGD', splits=[100, 0, 0], lr=1, num_of_epochs=1)
        self.assertListEqual([[-51.0]],test.model.all_parameters['W'].data.numpy().tolist())
        self.assertListEqual([-15.0], test.model.all_parameters['b'].data.numpy().tolist())
        self.assertListEqual([[-51.0]], test.model.all_parameters['a'].data.numpy().tolist())

    def test_network_linear_interpolation_train(self):
        NeuObj.clearNames()
        x = Input('x')
        param = Parameter(name='a', sw=1)
        rel1 = Fir(W=param)(Interpolation(x_points=[1.0, 2.0, 3.0, 4.0],y_points=[2.0, 4.0, 6.0, 8.0], mode='linear')(x.last()))
        out = Output('out',rel1)

        test = Modely(visualizer=None, seed=1)
        test.addModel('fun',[out])
        test.addMinimize('error', out, x.last())
        test.neuralizeModel(0.01)

        dataset = {'x':np.random.uniform(1,4,100)}
        test.loadData(name='dataset', source=dataset)
        test.trainModel(num_of_epochs=100, train_batch_size=10)
        self.assertAlmostEqual(test.model.all_parameters['a'].item(), 0.5, places=2)

    def test_multimodel_with_loss_gain_and_lr_gain(self):
        NeuObj.clearNames()
        ## Model1
        input1 = Input('in1')
        a1 = Parameter('a1', dimensions=1, tw=0.05, values=[[1],[1],[1],[1],[1]])
        output11 = Output('out11', Fir(W=a1)(input1.tw(0.05)))
        a2 = Parameter('a2', dimensions=1, tw=0.05, values=[[1], [1], [1], [1], [1]])
        output12 = Output('out12', Fir(W=a2)(input1.tw(0.05)))
        a3 = Parameter('a3', dimensions=1, tw=0.05, values=[[1], [1], [1], [1], [1]])
        output13 = Output('out13', Fir(W=a3)(input1.tw(0.05)))

        test = Modely(visualizer=None, seed=42)
        test.addModel('model1', [output11, output12, output13])
        test.addMinimize('error11', input1.next(), output11)
        test.addMinimize('error12', input1.next(), output12)
        test.addMinimize('error13', input1.next(), output13)

        ## Model2
        input2 = Input('in2')
        b1 = Parameter('b1', dimensions=1, tw=0.05, values=[[1],[1],[1],[1],[1]])
        output21 = Output('out21', Fir(W=b1)(input2.tw(0.05)))
        b2 = Parameter('b2', dimensions=1, tw=0.05, values=[[1],[1],[1],[1],[1]])
        output22 = Output('out22', Fir(W=b2)(input2.tw(0.05)))
        b3 = Parameter('b3', dimensions=1, tw=0.05, values=[[1],[1],[1],[1],[1]])
        output23 = Output('out23', Fir(W=b3)(input2.tw(0.05)))

        test.addModel('model2', [output21, output22, output23])
        test.addMinimize('error21', input2.next(), output21)
        test.addMinimize('error22', input2.next(), output22)
        test.addMinimize('error23', input2.next(), output23)
        test.neuralizeModel(0.01)

        data_in1 = [1, 1, 1, 1, 1, 2]
        data_in2 = [1, 1, 1, 1, 1, 2]
        dataset = {'in1': data_in1, 'in2': data_in2}

        test.loadData(name='dataset', source=dataset)

        ## Train only model1
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[1], [1], [1], [1], [1]])
        test.trainModel(optimizer='SGD', models='model1', splits=[100,0,0], lr=1, num_of_epochs=1)
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])

        ## Train only model2
        test.neuralizeModel(0.01, clear_model=True)
        test.trainModel(optimizer='SGD', models='model2', splits=[100,0,0], lr=1, num_of_epochs=1)
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])

        ## Train both models
        test.neuralizeModel(0.01, clear_model=True)
        test.trainModel(optimizer='SGD', models=['model1','model2'], splits=[100,0,0], lr=1, num_of_epochs=1)
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])

        ## Train both models but set the gain of a to zero and the gain of b to double
        test.neuralizeModel(0.01, clear_model=True)
        test.trainModel(optimizer='SGD', models=['model1','model2'], splits=[100,0,0], lr=1, num_of_epochs=1, lr_param={'a1':0, 'b1':2})
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[-11],[-11],[-11],[-11],[-11]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])

        ## Train both models but set the minimize gain of error1 to zero and the minimize gain of error2 to double
        test.neuralizeModel(0.01, clear_model=True)
        test.trainModel(optimizer='SGD', models=['model1','model2'], splits=[100,0,0], lr=1, num_of_epochs=1, minimize_gain={'error11':0})
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[1],[1],[1],[1],[1]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])

        ## Train both models but set the minimize gain of error1 to zero and the minimize gain of error2 to double
        test.neuralizeModel(0.01, clear_model=True)
        test.trainModel(optimizer='SGD', models=['model1','model2'], splits=[100,0,0], lr=1, num_of_epochs=1, minimize_gain={'error11':-1,'error22':2})
        self.assertListEqual(test.model.all_parameters['a1'].data.numpy().tolist(), [[7],[7],[7],[7],[7]])
        self.assertListEqual(test.model.all_parameters['b1'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['a2'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b2'].data.numpy().tolist(), [[-11],[-11],[-11],[-11],[-11]])
        self.assertListEqual(test.model.all_parameters['a3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])
        self.assertListEqual(test.model.all_parameters['b3'].data.numpy().tolist(), [[-5],[-5],[-5],[-5],[-5]])

    def test_train_equation_learner(self):
        NeuObj.clearNames()
        def func(x):
            return np.cos(x) + np.sin(x)
        
        data_x = np.random.uniform(0, 2*np.pi, 200)
        data_y = func(data_x)
        dataset = {'x': data_x, 'y': data_y}

        x = Input('x')
        y = Input('y')

        linear_in = Linear(output_dimension=5)
        linear_in_2 = Linear(output_dimension=5)
        linear_out = Linear(output_dimension=1, W_init=init_constant, W_init_params={'value':1})

        equation_learner = EquationLearner(functions=[Sin, Identity, Add, Cos], linear_in=linear_in)  ## W=1*5 , b=1, activation_out=4
        equation_learner2 = EquationLearner(functions=[Add, Identity, Mul],linear_in=linear_in_2, linear_out=linear_out) ## INGRESSO W=4*5, b=5, activation_out=3   USCITA W=3*1, b=1

        eq1 = equation_learner(x.last())
        eq2 = equation_learner2(eq1)
        out = Output('eq2', eq2)

        example = Modely(visualizer=TextVisualizer())
        example.addModel('model',[out])
        example.addMinimize('error', out, y.last())
        example.neuralizeModel()
        example.loadData(name='dataset', source=dataset)

        ## Print the initial weights
        optimizer_defaults = {'weight_decay': 0.3,}
        example.trainModel(train_dataset='dataset', lr=0.01, num_of_epochs=2, optimizer_defaults=optimizer_defaults)
