# lambdas = {
# "1,2":2.4434427,
# "1,3":2.2174664,
# "1,4":12.4170387,
# "1,5":15.4170585,
# "1,6":18.4170739,
# "1,7":21.4170681,
# "1,8":24.4170405,
# "1,9":27.4171464,
# "1,10":30.4171221,
# "1,11":6.6834151,
# "1,12":18.2085234,
# "1,13":19.7084819,
# "1,14":21.2084525,
# "1,15":22.7085382,
# "2,3":5.3932355,
# "3,4":2.8443067,
# "3,5":3.1339948,
# "3,7":2.9016732,
# "3,8":3.0893467,
# "3,10":2.9309436,
# "5,7":1.9607503,
# "5,8":5.1133148,
# "5,9":2.5288683}

lambdas = {
"1,2":2.4434427250699096,
"1,3":2.2174664768977426,
"1,4":12.417038747006254,
"1,5":15.417058504960167,
"1,6":18.417073925559762,
"1,7":21.41706814202711,
"1,8":24.417040571725813,
"1,9":27.417146437771752,
"1,10":30.41712211110694,
"1,11":6.683415162692536,
"1,12":18.208523431588784,
"1,13":19.708481975607533,
"1,14":21.20845259952416,
"1,15":22.70853824241943,
"2,3":5.393235598097941,
"3,4":2.844306703050331,
"3,5":3.13399485843738,
"3,7":2.9016732945413732,
"3,8":3.08934679122933,
"3,10":2.9309436043679087,
"5,7":1.960750369943171,
"5,8":5.113314806364161,
"5,9":2.5288683997372066,
"10010":3.2123750958101556,
"01001":2.5046387448555136,
"01010":3.4871112310078973}
    

for s in lambdas:
    b = lambdas[s]
    print(s)
    cf = continued_fraction(b)[:15]
    print(cf)
    for i in range(len(cf)):
        if(len(str(cf.convergent(i).numerator())) > 4):
            break
        cf.convergent(i)