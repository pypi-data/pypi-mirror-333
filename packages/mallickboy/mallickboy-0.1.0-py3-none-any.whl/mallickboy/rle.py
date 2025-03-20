
def compress_rle(user_input: str) -> list[str]:  # Run-Length Encoding (RLE)
    if not user_input:
        return 
    elif isinstance(user_input, str):
        chars = list(user_input)
    elif isinstance(user_input, list):
        chars = user_input
    else:
        raise TypeError("Input must be a string (str) or a list of characters(list(str))")
    # print(chars)
    if not isinstance(chars[0], str):
        raise TypeError("Input must be a string (str) or a list of characters(list(str))")
    
    # code starts from here
    i, N, count= 0, len(chars), 0
    if not N: return []
    fp=1        # as 0 index hold by appropriate character
    for i in range(1, N):
        if chars[i] ==chars[i-1]:
            count +=1
        else:
            if count:
                if count<9:
                    chars[fp], fp, count= str(count+1),fp+1,0 # new + old 
                else:
                    for ch in str(count+1):
                        chars[fp], fp= ch,fp+1
                    count=0

            chars[fp]= chars[i]
            fp +=1      # reset the count
        # print(chars, count)
    if count:
        if count<9:
            chars[fp], fp, count= str(count+1),fp+1, 0 # new + old 
        else:
            for ch in str(count+1):
                chars[fp], fp= ch,fp+1
            count=0
    for i in range(fp, N): chars.pop()
    return "".join(chars)


