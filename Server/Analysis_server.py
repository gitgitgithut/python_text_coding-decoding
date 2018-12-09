import GeneratorPolynomial
from math import *
import sys
import time
import os.path

def genQue():
    # Analysis Control Panel ===============================================================================================
    # Model parameters _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    # Choose which model to analyze. May be:
    #     'A' - Model A
    #     'B' - Model B
    #     'C' - Model C
    #     'AB'- Models A and B in series
    model_sel = 'A'
    # Length of randomly generated message
    message_len = 1000
    # Generator sequence for convolution encoding/decoding
    genSeq = GeneratorPolynomial.genSeqs[2][4]  # Index genSeqs with [rate][memory]. Goes up to [16][28]
    # Convolutional Codes, Klaus von der Heide
    # Order of Huffman convertor, or modified ASCII convertor
    Huff_order = 1  # Can be 1 or 2. For fixed length, set to 0
    # Number of bits encoded at once
    inRate = 1
    # Source symbols. For fixed length encoding, order determines mapping.
    alphabet = 'abcdefghijklmnopqrstuvwxyz******'
    # alphabet = 'eanshlufpyvxq******zjkbgwmcdriot'
    # alphabet = 'eumafonw*is*r**x*hdklvb*czqyjgpt'
    # alphabet = 'etaonisrhdlcumfwpgybvkxjqz******'
    # alphabet = 'etasorhpndlgcyb*iumvfkx*wjq*z***'
    # Analysis parameters _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    # Note: errors checked are logarithmically weighted towards the smaller errors.
    # Simulation starting epsilon
    epsilon_lo = 0.001
    # Simulation steps between epsilons (in powers)
    epsilon_dt = 1 / 20
    # Simulation is stopped at whichever is reached first, BSC epsilon of epsilon_hi, or error rate of error_high
    epsilon_hi = 0.5
    error_high = 1
    # Do overStep more points than the above parameters had indicated
    overStep = 1
    # Do underStep less points than the lower parameters had indicated
    underStep = 0
    # Number of trials to average over = Mcoeff*10^epsilon_exp/len(message), where epsilon = 10^-epsilon_exp
    Mcoeff = 100000
    # Target number of trials per data packet
    Mtarg = 1000
    '''
    # File path and name to backup data to. Replace back slashes with forward slashes, or with double back slashes. Save as a .txt file.
    filename = "C:/Users/antho/Desktop/Computer Files/Education/Queen's/4th Year/MTHE 493/term2/code/Model_2/Backup data/DataBackup0.txt"


    # Backup data file code_________________________________________________________________________________________________
    # Replace forward slashes with back slashes
    file = ''
    for char in filename:
        if char == '/':
            file += '\\'
        else:
            file += char
    while os.path.isfile(file):
        letter = file[-5]
        if letter == '9':
            letter = 'A'
        elif letter == 'Z':
            letter = 'Z0'
        else:
            letter = chr(ord(letter)+1)
        file = file[:-5] + letter + file[-4:]
    print('Saving to: \t'+file)
    saveFile = open(file,'w')
    saveFile.write('BSC Epsilon \tSymbol Error Rate \tVariance \tAverage Length Difference \tVariance\n')
    saveFile.close()
    '''
    # Analysis code_________________________________________________________________________________________________________
    # Setup error rates to test and number of trials (M) to average over. Small error rates need more trials. We'll be
    # plotting on a logarithmic scale, so we'll need more small error rates than big error rates.
    epsilon = []
    M = []
    M_count = 0
    M_limit = 0
    for i in range(-floor(log10(epsilon_lo) / epsilon_dt) + underStep,
                   -floor(log10(epsilon_hi) / epsilon_dt) - 1 - overStep, -1):
        epsilon.append(10 ** (-i * epsilon_dt))
        M.append(floor(Mcoeff * 10 ** (i * epsilon_dt) / message_len) + 1)
        M_limit += M[-1]
    #print('Max number of epsilons:        ' + str(len(epsilon)))
    #print('Total number of trials to run: ' + str(M_limit))
    #print('Start Time:                    ' + str(time.ctime(time.time())))

    # Arrange queue of data packets
    queue = []
    for i in range(0, len(M)):
        Mtemp1 = M[i]
        Mtemp2 = Mtemp1 // Mtarg
        if Mtemp2 == 0:
            Mtemp3 = 0
        else:
            Mtemp3 = (Mtemp1 % Mtarg) // Mtemp2
        Mtemp1 = Mtarg + Mtemp3
        if M[i] - Mtemp1 > 0:
            for j in range(0, Mtemp2 - 1):
                queue.append(str([model_sel, message_len, epsilon[i], Huff_order, inRate, alphabet, genSeq,
                                  Mtemp1, j]).replace(" ", ""))
                # print(queue[-1])
            queue.append(str([model_sel, message_len, epsilon[i], Huff_order, inRate, alphabet, genSeq,
                              M[i] - (j + 1) * Mtemp1, j + 1]).replace(" ", ""))
        elif M[i] - Mtemp1 <= 0:
            queue.append(str([model_sel, message_len, epsilon[i], Huff_order, inRate, alphabet, genSeq,
                              M[i], 0]).replace(" ", ""))
        else:
            continue

    #print(queue)
    return queue
        # print(M[i])

    # # Get data point distribution for n processes. Choose distribution index.
    # n = 4
    # i_n = 3
    # Msum = 0
    # Mlow = i_n*M_limit//n
    # Mhigh = (i_n+1)*M_limit//n
    # indices = []
    # for i in range(0,len(M)):
    #     Msum += M[i]
    #     if Msum > Mlow:
    #         break
    # for j in range(i,len(M)):
    #     Msum += M[j]
    #     indices.append(j)
    #     if Msum > Mhigh:
    #         break
    # print(indices)
    # print(M)
    '''

    # Estimate time to run model
    huffBook = ModelAInit(Huff_order)
    lastTime = time.time()
    message_out = ModelA(huffBook, message, 0.01, Huff_order, genSeq, inRate)
    seconds = (time.time()-lastTime)*M_limit
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    minutes = minutes % 60
    if minutes < 10:
        print('Estimated run time(h:mm):      ' + str(hours) + ':0' + str(minutes))
    else:
        print('Estimated run time(h:mm):      ' + str(hours) + ':' + str(minutes))
    start_time = time.time()
    print('Estimated Finish Time:         ' + str(time.ctime(seconds+lastTime)))

    # Run model M times and get average error rate, for each error rate
    lastTime = 0
    timeCount = 0
    timeVarCount = 0
    error_rate = []
    error_rateVar = []
    lendiff = []
    lendiffVar = []
    for i in range(0,len(epsilon)):
        error_rateCount = 0
        error_rateVarCount = 0
        timeCount = 0
        timeVarCount = 0
        lendiffCount = 0
        lendiffVarCount = 0
        for j in range(0, M[i]):
            lastTime = time.time()
            message_out = ModelA(huffBook, message, epsilon[i], Huff_order, genSeq, inRate)
            lastTime = time.time() - lastTime
            timeCount += lastTime
            timeVarCount += lastTime**2
            error = findErrorRate(message, message_out)
            error_rateCount += error[0]
            error_rateVarCount += error[0]**2
            lendiffCount += error[1]
            lendiffVarCount += error[1]**2
        M_count += M[i]

        error_rate.append(error_rateCount/M[i])
        error_rateVar.append((error_rateVarCount-(error_rateVarCount/M[i])**2)/M[i])
        lendiff.append(lendiffCount / M[i])
        lendiffVar.append((lendiffVarCount - (lendiffVarCount / M[i]) ** 2) / M[i])

        saveFile = open(file, 'a')
        saveFile.write(str(epsilon[i])+'\t'+str(error_rate[i])+'\t'+str(error_rateVar[i])
              +'\t'+str(lendiff[i])+'\t'+str(lendiffVar[i])+'\n')
        saveFile.close()

        print("{:.2f}%,  \t\t error rate {:f}".format(M_count / M_limit * 100, error_rate[-1]))
        if error_rate[-1] > error_high:
            break

    # Print up the error rate data.
    print('BSC Epsilon \tSymbol Error Rate \tVariance \tAverage Length Difference \tVariance')
    for i in range(0,len(error_rate)):
        print(str(epsilon[i])+'\t'+str(error_rate[i])+'\t'+str(error_rateVar[i])
              +'\t'+str(lendiff[i])+'\t'+str(lendiffVar[i]))

    # Print up inputs and calculated metrics.
    huffrate = Huffman.makeHuffDict(Huffman,letterBook[Huff_order-1])
    huffrate = Huffman.HuffRate(Huffman,letterBook[Huff_order-1],huffrate)
    memory = 0
    for poly in genSeq:
        if floor(log(poly,2)) > memory:
            memory = floor(log(poly,2))
    stats = 'Model A'
    stats += '\nHuffman order: \t' + str(Huff_order)
    stats += '\nHuffman rate (bits/symbol): \t'+str(huffrate)
    stats += '\nGenerator sequence: \t' + str(genSeq)
    stats += '\nMemory: \t' + str(memory)
    stats += '\nRegister input rate: \t' + str(inRate)
    stats += '\nConvolution encoder rate (bits/chnl_use): \t' + str(inRate/len(genSeq))
    stats += '\nSystem Code rate (symbols/chnl_use): \t' + str(inRate/len(genSeq)/huffrate)
    stats += '\nMessage Length: \t' + str(len(message))
    stats += '\nDecode Time(s): \t' + str(timeCount/M_limit)
    stats += '\nDecode Time(s) Variance: \t' + str((timeCount - (timeVarCount / M_limit) ** 2) / M_limit)
    stats += '\nBSC epsilon range: \t' + str((epsilon_lo,epsilon_dt,epsilon_hi))
    stats += '\nSup symbol error rate: \t' + str(error_high)
    stats += '\nMcoeff: \t'+str(Mcoeff)
    print(stats)
    saveFile = open(file, 'a')
    saveFile.write(stats)
    saveFile.close()
    print()
    print()
    end_time = time.time()-start_time
    seconds = end_time
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    minutes = minutes % 60
    if minutes < 10:
        print('Total time taken(h:mm): \t' +str(hours)+':0'+str(minutes))
    else:
        print('Total time taken(h:mm): \t' +str(hours)+':'+str(minutes))
        '''

genQue()
