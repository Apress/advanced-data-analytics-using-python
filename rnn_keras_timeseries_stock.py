'''
Created on Aug 1, 2017

'''
#import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import sys
np.random.seed(1234)


def read_data(path_to_dataset,
                           sequence_length=50,
                           ratio=1.0):

    max_values = ratio * 2049280

    with open(path_to_dataset) as f:
        data = csv.reader(f, delimiter=",")
        power = []
        nb_of_values = 0
        for line in data:
            #print(line)
            #if nb_of_values == 3500:
             #   break
            try:
                power.append(float(line[1]))
                nb_of_values += 1
            except ValueError:
                pass
            # 2049280.0 is the total number of valid values, i.e. ratio = 1.0
            if nb_of_values >= max_values:
                break
    return power

def convert_to_categorical_increasing(current, future):
	change = (future-current)*100/current
	if change > 0.005:
		return 1
	else:
		return 0

def convert_to_categorical_decreasing(current, future):
        change = (future-current)*100/current
	if change < 0.005:
		return 0
	else:
		return 1

def create_matrix(y_train):
	y = [[0 for i in xrange(2)] for j in xrange(len(y_train))]
	for i in range(len(y_train)):
		#print y_train[i]
		y[i][y_train[i]] = 1
	return y
		

def process_data(power, sequence_length, ratio, increasing, error):
    #print("Data loaded from csv. Formatting...")
    #fig = plt.figure()
    #plt.plot(power)
    #plt.show()
    result = []
    if not error:
    	for i in range(len(power)-1):
		if increasing:
			power[i] = convert_to_categorical_increasing(power[i], power[i+1])
		else:
			power[i] = convert_to_categorical_decreasing(power[i], power[i+1])
    for index in range(len(power) - sequence_length-1):
        result.append(power[index: index + sequence_length])
    result = np.array(result)  # shape (2049230, 50)

    #result = np.log(result+1)
    #print result
    #exit(0)
#     print ("Shift : ", result_mean)
    #print ("Data  : ", result.shape)
    
    row = int(round(0.9 * result.shape[0]))
    #:print row
    train = result[:row, :]
    np.random.shuffle(train)
    X_train = train[:, :-1]
    y_train_temp = train[:, -1]
    #print y_train_temp
    y_train = create_matrix(y_train_temp)
    X_test = result[row:, :-1]
    y_test = result[row:, -1]

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    return [X_train, y_train, X_test, y_test]


def build_model():
    model = Sequential()
    layers = [1, 100, 50, 2]

    model.add(LSTM(
        layers[1],
        input_shape=(None, layers[0]),
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        layers[3]))
    model.add(Activation('softmax'))

    start = time.time()
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    #print ("Compilation Time : ", time.time() - start)
    return model


def run_network(data=None, increasing=False, error=False):
    global_start_time = time.time()
    epochs = 2
    ratio = 0.5
    sequence_length = 100

    X_train, y_train, X_test, y_test = process_data(
            data, sequence_length, ratio,increasing, error)

    #print ('\nData Loaded. Compiling...\n')

    model = build_model()

    try:
        model.fit(
            X_train, y_train,
            batch_size=512, nb_epoch=epochs, validation_split=0.05, verbose=0)
        predicted = model.predict(X_test)
        #predicted = np.reshape(predicted, (predicted.size,))
    except KeyboardInterrupt:
        #:print ('Training duration (s) : ', time.time() - global_start_time)
        return model, y_test, 0

    try:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(y_test[:100]*result_max)
        plt.plot(predicted[:100]*result_max)
        plt.show()
    except Exception as e:
	pass
        #print (str(e))
    #print ('Training duration (s) : ', time.time() - global_start_time)
    
    return y_test, predicted


if __name__ == '__main__':
    path_to_dataset = 'data/CLSB Comdty.csv'#'data/20170818/CLSB Comdty.csv'
    data = read_data(path_to_dataset)
    #print len(data)
    success = 0
    fail = 0
    success1 = 0
    fail1 = 0
    false_low = 0
    false_high = 0
    error  = []
    err_predicted = {}
    mean_std_inc = 0
    mean_std_dec = 0
    mean_std_err = 0
    e = False
    count = 0
    count_bad = 0
    for i in range(0,len(data)-1000,89):
	count = count + 1
	if count_bad >=2:
		count_bad = 0
		K = 1
		continue
	#success = 0
        #fail = 0
        #false_low = 0
        #false_high = 0
        d1 = data[i:i+1001]
        d2 = data[i:i+1001]
        y_test_increasing, predicted_increasing = run_network(d1, True, False)
	y_test_decreasing, predicted_decreasing = run_network(d2, False, False)
	if count > 11 and len(error) >= 1000:
                err_test, err_predicted = run_network(error, True, True)
		#print "error predicted"
	prob_increasing = predicted_increasing[:,1]
	increasing_mean = prob_increasing.mean()
	increasing_std = prob_increasing.std()
	prob_decreasing = predicted_decreasing[:,0]
	decreasing_mean = prob_decreasing.mean()
	decreasing_std = prob_decreasing.std()
	if i > 0:
                mean_std_inc = (mean_std_inc + increasing_std)/2
                mean_std_dec = (mean_std_dec + decreasing_std)/2
        else:
                mean_std_inc = increasing_std
                mean_std_dec = decreasing_std

	y_test_decreasing -= 1
	prob_err = []
	prob_err_mean = 0
	prob_err_std = 0
        if count > 11 and len(error) >= 1000:
		prob_err = err_predicted[:,0]
		prob_err_mean = prob_err.mean()
		prob_err_std = prob_err.std()
                error = error[90:]
		#print "mean calculated"
		#print prob_err
	#if i > 11 and len(error_increasing) >= 1000 and len(err_predicted_increasing)>=90:
	if True:
		mean_std_err = 0
		K = 1
		K1 = 1
		if success != 0:
			acc_with = success*100/(success + fail)
			#acc_wo = success1*100/(success1 + fail1)
			print acc_with
			if acc_with < 58 and success != 0:
				K = K/2
				count_bad = count_bad + 1
				#mean_std_inc = 0
				#mean_std_dec = 0
				if K1 == 1:
					K1 = 1.5
				else:
					K1 = 1
			if acc_with > 58:
				K = 1/2
				#mean_std_err = 0
			if mean_std_err == 0:
				mean_std_err = prob_err_std
			else:
				mean_std_err = (prob_err_std + mean_std_err)/2
		for j in range(len(y_test_decreasing)-1):
			ac_status = y_test_increasing[j] + y_test_decreasing[j]
			pr_status = 0
			if True:
				inc = (prob_increasing[j] - increasing_mean + K1*mean_std_inc)
				dec = (prob_decreasing[j] - decreasing_mean + K1*mean_std_dec)
				#print inc,dec
				if inc > 0 or dec > 0:
					if inc > dec:
						pr_status = 1 
					else:
						pr_status = -1 
				else:
					pr_status = 0 
				if ac_status != pr_status:
					error.append(0)
				else:
					error.append(1)
				if ac_status != 0:
					if inc > 0 and dec > 0:
						continue
					if count >= 10 and len(error) >= 1000 and len(err_predicted)>=90:
						if ac_status == pr_status:
 	                                       		success1 = success1 + 1
                                        	else:
         	                                	fail1 = fail1 + 1
						if (prob_err[j] - prob_err_mean) > K*mean_std_err:
							pr_status = -1*pr_status
						else:
							if ac_status == pr_status:
								success = success + 1
							else:
								fail = fail + 1 
					#else:
					#	success = success1
					#	fail = fail1
					#print ac_status,',',pr_status, ',',prob_increasing[j],',',prob_decreasing[j]
		print success,',',fail,',',count #success1,',',fail1,',', count  #,',',false_high,',',false_low #,',',increasing_std,',',decreasing_std,',',increasing_mean,',',decreasing_mean
