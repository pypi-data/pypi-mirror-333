import time, tracemalloc
def runtime(function=None, show_log=True, return_info=False):
    if function is None:  # @runtime()  # if no function is passed, memory location of the function is same as of the None, so returning a decorator that takes function as an argument
        return lambda function: runtime(function, show_log, return_info) # passing show and get_time to the wrapper
    def wrapper(*args, **kwargs):
        start_time= time.time()
        tracemalloc.start()     # noting start time
        initial_memory, _ = tracemalloc.get_traced_memory() # noting initial MEM status

        result= function(*args, **kwargs)       # main function execution

        final_memory, peak_memory = tracemalloc.get_traced_memory() # noting Final MEM status
        duration= round((time.time()- start_time)* 1000, 3)   # final time
        tracemalloc.stop()
        space_occupied = round((final_memory- initial_memory)/ 1024**2, 3)    # byte to MB
        space_released= round((peak_memory- final_memory)/1024**2,3)    # byte to MB
        space_peak_usage= round((peak_memory- initial_memory)/1024**2,3)    # byte to MB
        if show_log :
            print(f"\nRuntime Report for '{function.__name__}':\n"
                f"- Memory Used During Execution : {space_peak_usage} MB\n"
                f"- Memory Currently Occupied    : {space_occupied} MB\n"
                f"- Memory Freed After Execution : {space_released} MB\n"
                f"- Time Required for Execution  : {duration} ms\n")
        if return_info:
            return result, ((space_peak_usage, space_occupied, space_released), duration)
        return result
    return wrapper