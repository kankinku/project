할일

1. 시간표 인식하기 
( 화 12 수 3 )

class_time = list(map(str,input().split()))

월 1 2
{월 : 1,2}

for o in range(len(class_time)):
    # 0과 1을 수동 입력해주기
    if i % 2 == 0:
        짝수는 시간
        홀수는 요일
        -> 딕셔너리로 저장

DB 수정 필요 ( 목요일에 할게요 ) <- class_time을 딕셔너리로 만들어야함
DB에 class_info 삽입 수정 필요

---

{월 : 1,2}

DB에서 데이터 불러서 dashborad에 표시 


        <div class="part__day">
            <span class="time">9am <br> - <br> 10pm</span>
            <div class="task"></div>
            <div class="task"></div>
            <div class="task"></div>
            <div class="task"></div>
            <div class="task"></div>
            <div class="task"></div>
            <div class="task"></div>
        </div>


이런 형식으로 저장되어 있는데 7로 나눠서 몇번째 part__day인지 nth_children(?)으로 불러서
그 속에서 n번재 task의 색을 칠해야한다.


---


학점 계산기 
1. 시간 계산해서 불러오기 
2. 