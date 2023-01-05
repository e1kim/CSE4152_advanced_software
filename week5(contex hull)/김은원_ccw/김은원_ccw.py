#import numpy as np

def display(input_txt_path, output_txt_path):
    import matplotlib.pyplot as plt
    
    '''
    input1 : input_txt_path = path of input_example.txt
    input2 : output_txt_path = path of output_example.txt
    return : save convex_hull image
    '''
    
    with open(input_txt_path, "r") as f:
        input_lines = f.readlines()
    with open(output_txt_path, "r") as f:
        output_lines = f.readlines()
        
    whole_points = input_lines
    area = round(float(output_lines[0]), 1)
    hull_points = output_lines[1:]
    
    
    x_list = [int(x.split(" ")[0]) for x in whole_points]
    y_list = [int(x.split(" ")[1]) for x in whole_points]
    plt.plot(x_list, y_list, marker='.', c='y',linestyle='None')
    
    hx_list = [int(x.split(" ")[0]) for x in hull_points]
    hy_list = [int(x.split(" ")[1]) for x in hull_points]
  
    plt.plot(hx_list, hy_list, marker='*', linestyle='None', markersize=10, c='r')
    

    title = plt.title(f'Area : {area}')
    plt.setp(title, color='r')
    plt.savefig(output_txt_path[:-3]+"png", bbox_inches='tight')
    plt.clf()

def is_inside(polygon,point):

        def cross(p1,p2):
            x1, y1 = p1
            x2, y2 = p2
            differ_y = y1-y2
            differ_x = x1-x2
            
            if differ_y == 0:
                #print("y가같음")
                if y1 == point[1] :
                    if min(x1,x2)  <= point[0] <=max(x1,x2):
                        return 1, True
                return 0,False

            if differ_x==0:
                #print("x가같음")
                if min(y1,y2)  <= point[1] <=max(y1,y2):
                    if point[0] <= x1:
                        return 1, point[0] == max(x1,x2)
                return 0,False
            
            a = differ_y / differ_x
            b = y1 - x1*a
            x = point[1] - b
            x /= a
            
            if point[0] <= x:
                #print("대각선")
                if min(y1,y2) <= point[1] <=max(y1,y2):
                    return 1,point[0] == x or point[1] in (y1,y2)

            #print("nothing")
            return 0,False
        
        cross_points = 0
        for m in range(len(polygon)):
            #print(m,"번째","점:",point,"다각형점1",polygon[m], "다각형점2",polygon[m-1])
            num, on_line = cross(polygon[m],polygon[m-1])
            if on_line:
                return 0
            cross_points += num

        return cross_points%2


def cross_product(p1,p2,p3):
    return ((p2[0] - p1[0]) * (p3[1]- p1[1]) - (p2[1] - p1[1]) * (p3[0]- p1[0]))

def dot(p1,p2,p3):
    return ( p1[0]*p2[0] + p1[1]*p2[1])
def cross(p1,p2):
    return (p1[0]*p2[1] - p1[1]*p2[0])

def get_slope(p1,p2):
    if p1[0] == p2[0]:
        return float('inf')
    else:
        return 1.0 * (p1[1]-p2[1])/(p1[0]-p2[0])


for file_number in range(3):
    
    fp_r = open("input%d.txt"%(file_number+1),'r')

    points =[]



    for s in fp_r:
        num = list(int(x) for x in s.split() )
        points.append(num)
        
        
    #print("init: ",points)
    hull = []
    #y값을 기준으로 오름차순 정렬 
    points=sorted(points, key=lambda points: points[1])
    #print(points)

    #시작점
    start = points.pop(0)
    
    #기울기 기준으로 정렬
    points.sort(key=lambda p:(get_slope(p,start),-p[1],p[0]) )

    index=0
    for i in range(len(points)):
        if get_slope(points[i],start) > 0:
            index = i
            break
    points = points[index:] +points[:index] 

    #print("기울기기준정렬",points)


    hull.append(start)
    for point in points:
        while(len(hull)>1) and cross_product(hull[-2],hull[-1],point)<=0:
            hull.pop()
        hull.append(point)
      

    


    #넓이 구하기
    answer=0

    for i in range(len(hull)):  
        if i == len(hull)-1:
           answer += (hull[i][0]*hull[0][1] - hull[0][0]*hull[i][1])
        else:
            answer += ( hull[i][0]*hull[i+1][1] - hull[i+1][0]*hull[i][1])    
    area = abs(answer)/2
    print("넓이: ",area)


    #파일 쓰기
    fp_w = open("김은원_output%d.txt"%(file_number+1),'w')

    print(area,file=fp_w)

    for i in range(len(hull)):
        print(hull[i][0],hull[i][1],file=fp_w)

    fp_r.close()
    fp_w.close()


    #cross_point = 겹치는 점의 수이고 ins_inside는return 1 이면 내부, 0이면 외부인걸확인하는함수



    fp_r2 = open("김은원_output%d.txt"%(file_number+1),'r')
    num_point =0
    polygon=[]
    for s in fp_r2:
        if num_point==0: num_point +=1; continue
        num = list(int(x) for x in s.split() )
        polygon.append(num)
        num_point +=1
    #print("다각형 점들:",polygon)

    fp_r2point = open("point_in_polygon_input.txt",'r')
    fp_r2print = open("김은원_point_in_polygon_output%d.txt"%(file_number+1),'w')
    input_points = []

    for s in fp_r2point:
        num = list(int(x) for x in s.split() )
        input_points.append(num)
    #print("check point: ",input_points)


    for k in range(len(input_points)):
        if is_inside(polygon,input_points[k]) == 0:
            print("out",file = fp_r2print)
        else:
            print("in",file=fp_r2print)

    fp_r2.close()
    fp_r2point.close()
    fp_r2print.close()
    #if __name__ == "__main__":
    input_txt_path = ("input%d.txt"%(file_number+1))
    output_txt_path = ("김은원_output%d.txt"%(file_number+1))
    display(input_txt_path, output_txt_path)
    
    
