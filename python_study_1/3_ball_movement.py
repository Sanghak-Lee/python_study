import os
import pygame

############################################################################
# 기본초기화 (반드시 해야 하는 것들)
pygame.init() #초기화

#화면크기설정
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

#화면타이틀 설정
pygame.display.set_caption("그래 이거야")

#FPS
clock = pygame.time.Clock()
############################################################################



# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") #images 폴더 경로 반환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background1.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터 그리기

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character_right_1.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height
character_to_x = 0
character_speed = 10

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 여러발
weapons = []
weapon_speed = 10

# 공 만들기
ball_image=[pygame.image.load(os.path.join(image_path, "balloon1.png")),
            pygame.image.load(os.path.join(image_path, "balloon2.png")),
            pygame.image.load(os.path.join(image_path, "balloon3.png")),
            pygame.image.load(os.path.join(image_path, "balloon4.png"))
            ]
ball_speed_y = [-18, -15, -12, -9]
balls = []

#최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50,   #공의 x좌표
    "pos_y" : 50,   #공의 y좌표
    "img_idx" : 0,  #공의 이미지 인덱스
    "to_x" : 3,     #공의 x축 이동방향
    "to_y" : -6,    #공의 y축 이동방향
    "init_spd_y" : ball_speed_y[0] #y의 최초속도

})

a=0
b=0
running = True #게임 진행중인가?

while(running):
    dt = clock.tick(60) #게임화면의 초당 프레임 수를 결정
    
    # 2. 이벤트 처리(키보드, 마우스)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        
        if(event.type == pygame.QUIT): #창이 닫히는 이벤트가 발생하였는가?
            running = False
        if event.type == pygame.KEYDOWN:
           
           if event.key == pygame.K_LEFT:
               character_to_x -= character_speed
               if a== 0 :
                   a=1
                   character = pygame.image.load(os.path.join(image_path, "character_left_1.png"))
                   
               elif a == 1:
                    character = pygame.image.load(os.path.join(image_path, "character_left_2.png"))
                    a=0
           elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
                if b==0:
                   b=1
                   character = pygame.image.load(os.path.join(image_path, "character_right_1.png"))
                elif b ==1 :
                    character = pygame.image.load(os.path.join(image_path, "character_right_2.png"))
                    b=0
           elif event.key == pygame.K_SPACE: #무기발사
               weapon_x_pos = character_x_pos + character_width/2 - weapon_width
               weapon_y_pos = character_y_pos
               weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의            
    character_x_pos += character_to_x

    if character_x_pos<0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos =  screen_width - character_width
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] 
   
    # 천장에 닿은 무기 제거
    weapons = [  [  w[0], w[1]  ] for w in weapons if w[1] >0]


    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"] 
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_image[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을때
        if ball_pos_x <= 0 or ball_pos_x >= screen_width - ball_width:
            ball_val["to_x"] *= -1 

        #세로벽에 닿았을때
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] 
        else :
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] +=ball_val["to_x"] 
        ball_val["pos_y"] +=ball_val["to_y"] 
    # 4. 충돌 처리

    # 5. 화면에 그리기

    screen.blit(background, (0,0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos, weapon_y_pos))    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_image[ball_img_idx], (ball_pos_x, ball_pos_y))



    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
 


    pygame.display.update() #게임하면 다시 그리기


# 6. pygame 종료
pygame.quit()   