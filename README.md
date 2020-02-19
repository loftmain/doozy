doozy
=====

---

doozy는 주가 예측 분석 시뮬레이션 툴입니다.  
scikit-learn기반의 Random forest, K-NN, XGboost알고리즘을 사용하여 주가 분석을 한 후, zipline을 사용하여 전략의 성능을 테스팅할 수 있습니다.  
또한 백테스팅 결과를 가지고 수익률, 자산변동추이 그래프 차트를 확인할 수 있는 GUI 분석 툴입니다.

Features
--------

-	GUI환경을 제공:  
-	Codeless:  
-	복잡한 환경 세팅 없음:  
-	주가 분석을 기계학습으로:  

Install
-------

doozy는 복잡한 파이썬 환경을 세팅 할 필요 없이 [docker](https://www.docker.com)환경을 지원합니다. 간단하게 docker를 사용하여 doozy의 모든 기능을 사용할 수 있습니다.

#### docker

window환경:  
[VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/) 설치합니다.  
docker 실행 후에 window power shell에서

1.	도커 이미지 pull  
	`docker pull loftmain/doozy:0.2`

2.	window 환경변수 세팅  
	`set-variable -name DISPLAY -value YOUR-IP:0.0`

3.	도커 컨테이너 실행  
	`docker run -it -e DISPLAY=$DISPLAY -v /c/User:/data loftmain/doozy:0.2`

끝!  
간단해!!

Demo
----

[![Video Label](http://img.youtube.com/vi/4dJeh_nfYN4/0.jpg)](https://www.youtube.com/watch?v=4dJeh_nfYN4?t=0s)

developer
---------
