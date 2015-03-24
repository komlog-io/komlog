'''
In this file we declare the different permissions that 
can be applied to an element 
'''


ALL           =  0b11111111111111111111111111111111
NONE          =  0b00000000000000000000000000000000
CAN_READ      =  0b00000000000000000000000000000001
CAN_EDIT      =  0b00000000000000000000000000000010
CAN_DELETE    =  0b00000000000000000000000000000100
CAN_SHARE     =  0b00000000000000000000000000001000
CAN_SNAPSHOT  =  0b00000000000000000000000000010000