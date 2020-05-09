# For the consistant usage of Agent Data.
# Might not be neccessary

"""
At this stage, I am trying to pass in the car object to the validation module
so that the main module no longer has control over it. DONE
There is no reason for the main module to know who just used the 
vehicle, so this reduces the need for the main module to know more
than the car that it is operating in. DONE
As such, I should move the information from main to validation, or as much 
as is possible. DONE
This way, if a valid user is loaded, then the car can be passed into
the operational section for any usage of the variables. This SHOULD
remove the need for a carlocked variable.... DONE
"""