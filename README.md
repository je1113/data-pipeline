# Toy Data Pipeline

🚀 **시각적 ETL 데이터 파이프라인 구축 솔루션**

ETL 도구를 웹 기반으로 제공하는 오픈소스 프로젝트입니다. 
드래그앤드롭 인터페이스를 통해 누구나 쉽게 데이터 파이프라인을 설계하고 실행할 수 있으며, 
벡터 데이터베이스를 지원하여 RAG 모델 학습 데이터로 활용할 수 있습니다.

## ✨ 주요 기능

### 🎨 시각적 파이프라인 빌더
- 드래그앤드롭으로 간편한 파이프라인 설계
- 실시간 데이터 흐름 시각화
- 노드 기반 ETL 구성 (Extract → Transform → Load)

### 📊 다양한 데이터 소스 지원
- **Excel 파일**: 업로드 및 자동 파싱
- **RDBMS**: PostgreSQL, MySQL, SQLite 연결
- **벡터 DB**: Pinecone, Weaviate, ChromaDB 지원

### 🔄 유연한 데이터 변환
- Filter, Join, Map, Aggregation 기본 기능
- 사용자 정의 Python 스크립트 지원
- 실시간 데이터 미리보기

### 🤖 AI/RAG 특화 기능
- 텍스트 임베딩 자동 생성
- 문서 청킹 및 메타데이터 관리
- 벡터 검색 테스트 도구

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Infrastructure │
│                 │    │                 │    │                 │
│ React + TS      │◄──►│ FastAPI         │◄──►│ PostgreSQL      │
│ React Flow      │    │ SQLAlchemy      │    │ Redis           │
│ Material-UI     │    │ Celery          │    │ Vector DBs      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 빠른 시작

### 1. 사전 요구사항
- Docker & Docker Compose
- Node.js 18+ (로컬 개발 시)
- Python 3.11+ (로컬 개발 시)

### 2. 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/your-org/toy-data-pipeline.git
cd toy-data-pipeline

# Docker Compose로 전체 서비스 실행
docker-compose up -d

# 서비스 확인
docker-compose ps
```

### 3. 서비스 접속
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Flower (작업 모니터링)**: http://localhost:5555

## 🛠️ 개발 환경 설정

### Backend 개발 환경

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn main:app --reload
```

### Frontend 개발 환경

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 📁 프로젝트 구조

```
toy-data-pipeline/
├── frontend/              # React + TypeScript 앱
│   ├── src/
│   │   ├── components/    # UI 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── hooks/         # React Hooks
│   │   ├── store/         # Redux 상태 관리
│   │   └── utils/         # 유틸리티 함수
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI 백엔드
│   ├── app/
│   │   ├── api/           # API 라우터
│   │   ├── core/          # 설정 및 보안
│   │   ├── db/            # 데이터베이스 모델
│   │   ├── services/      # 비즈니스 로직
│   │   └── workers/       # Celery 작업
│   ├── requirements.txt
│   └── main.py
├── shared/                # 공통 타입 정의
├── docs/                  # 프로젝트 문서
├── docker/                # Docker 설정 파일
├── docker-compose.yml     # 개발환경 구성
└── README.md
```

## 🧪 테스트

### Backend 테스트
```bash
cd backend
pytest --cov=app tests/
```

### Frontend 테스트
```bash
cd frontend
npm run test
```

### E2E 테스트
```bash
npm run test:e2e
```

## 📈 개발 로드맵

### Phase 1: MVP (3개월)
- [x] 프로젝트 초기 설정
- [ ] 시각적 파이프라인 빌더
- [ ] Excel/DB 데이터 소스 연동
- [ ] 기본 Transform 기능
- [ ] Load 기능
- [ ] 실행 엔진

### Phase 2: 고급 기능 (2개월)
- [ ] 벡터 DB 연동
- [ ] 템플릿 라이브러리
- [ ] 스케줄링 시스템
- [ ] 사용성 개선

### Phase 3: 엔터프라이즈 (3개월+)
- [ ] 사용자 권한 관리
- [ ] REST API
- [ ] 고급 모니터링
- [ ] AI 기능 강화

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 개발 가이드라인
- TypeScript 사용 (Frontend)
- Type hints 사용 (Backend)
- 테스트 커버리지 80% 이상
- 코드 리뷰 필수

## 📚 문서

- [API 문서](http://localhost:8000/docs)
- [개발자 가이드](./docs/developer-guide.md)
- [아키텍처 문서](./docs/architecture.md)
- [배포 가이드](./docs/deployment.md)

## 🐛 버그 리포트 & 기능 요청

Issues 탭에서 버그 리포트나 기능 요청을 제출해주세요.

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- [React Flow](https://reactflow.dev/) - 시각적 다이어그램 라이브러리
- [FastAPI](https://fastapi.tiangolo.com/) - 고성능 Python 웹 프레임워크
- [Material-UI](https://mui.com/) - React UI 컴포넌트 라이브러리

## 📞 연락처

프로젝트 관련 문의: [이메일](mailto:contact@example.com)

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
