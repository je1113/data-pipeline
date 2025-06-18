# 개발자 가이드

## 개발 환경 설정

### 1. 사전 요구사항
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### 2. 로컬 개발 환경 설정

#### 자동 설정 (권장)
```bash
# 저장소 클론
git clone https://github.com/your-org/toy-data-pipeline.git
cd toy-data-pipeline

# 개발 환경 자동 시작
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh
```

#### 수동 설정

##### Backend 설정
```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값들을 설정

# 데이터베이스 및 Redis 시작
docker-compose up -d postgres redis

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 시작
uvicorn main:app --reload
```

##### Frontend 설정
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 시작
npm run dev
```

## 프로젝트 구조

```
toy-data-pipeline/
├── frontend/                 # React + TypeScript
│   ├── src/
│   │   ├── components/       # 재사용 가능한 UI 컴포넌트
│   │   ├── pages/           # 페이지 컴포넌트
│   │   ├── hooks/           # 커스텀 React Hooks
│   │   ├── store/           # Redux 상태 관리
│   │   ├── services/        # API 서비스
│   │   ├── utils/           # 유틸리티 함수
│   │   └── types/           # TypeScript 타입 정의
│   └── public/              # 정적 파일
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── api/             # API 엔드포인트
│   │   ├── core/            # 설정 및 보안
│   │   ├── db/              # 데이터베이스 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   └── workers/         # Celery 작업
│   ├── tests/               # 테스트 코드
│   └── alembic/             # 데이터베이스 마이그레이션
├── shared/                  # 공통 타입 및 유틸리티
├── docs/                    # 프로젝트 문서
└── scripts/                 # 개발 스크립트
```

## 개발 가이드라인

### 코딩 스타일

#### Frontend (TypeScript/React)
- **Prettier + ESLint** 사용
- **함수형 컴포넌트** + **Hooks** 사용
- **Material-UI** 컴포넌트 사용
- **명명 규칙**: PascalCase (컴포넌트), camelCase (변수/함수)

```typescript
// 컴포넌트 예시
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

const MyComponent: React.FC<Props> = ({ title, onSubmit }) => {
  const [isLoading, setIsLoading] = useState(false);
  
  return (
    <Box>
      <Typography variant="h6">{title}</Typography>
    </Box>
  );
};
```

#### Backend (Python/FastAPI)
- **Black + isort + flake8 + mypy** 사용
- **Type hints** 필수
- **Pydantic** 모델 사용
- **명명 규칙**: snake_case

```python
# API 엔드포인트 예시
from fastapi import APIRouter, Depends
from app.schemas.pipeline import PipelineCreate, PipelineResponse

router = APIRouter()

@router.post("/", response_model=PipelineResponse)
async def create_pipeline(
    pipeline: PipelineCreate,
    db: Session = Depends(get_db)
) -> PipelineResponse:
    """파이프라인 생성"""
    return await pipeline_service.create(db, pipeline)
```

### Git 워크플로우

#### 브랜치 전략
- `main`: 프로덕션 배포
- `develop`: 개발 통합
- `feature/*`: 기능 개발
- `hotfix/*`: 긴급 수정

#### 커밋 메시지 규칙
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**타입:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 변경
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드 프로세스 변경

**예시:**
```
feat(pipeline): add visual pipeline builder component

- Implement drag & drop functionality
- Add node connection system
- Support for Extract, Transform, Load nodes

Closes #123
```

### 테스트

#### Backend 테스트
```bash
# 단위 테스트
pytest tests/unit/

# 통합 테스트
pytest tests/integration/

# 커버리지 포함
pytest --cov=app tests/
```

#### Frontend 테스트
```bash
# 단위 테스트
npm run test

# 커버리지 포함
npm run test:coverage

# E2E 테스트
npm run test:e2e
```

### 디버깅

#### Backend 디버깅
1. **VS Code 설정** (`.vscode/launch.json`):
```json
{
  "name": "FastAPI Debug",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/backend/main.py",
  "console": "integratedTerminal",
  "envFile": "${workspaceFolder}/backend/.env"
}
```

2. **로깅 사용**:
```python
import structlog

logger = structlog.get_logger()
logger.info("Pipeline created", pipeline_id=pipeline.id)
```

#### Frontend 디버깅
1. **React DevTools** 설치
2. **Redux DevTools** 사용
3. **브라우저 DevTools** 활용

### 성능 최적화

#### Backend
- **비동기 처리**: `async/await` 사용
- **데이터베이스**: 인덱스 적절히 사용
- **캐싱**: Redis 활용
- **배치 처리**: Celery 사용

#### Frontend
- **Code Splitting**: React.lazy 사용
- **메모이제이션**: useMemo, useCallback 활용
- **가상화**: 대용량 데이터 테이블에 적용
- **이미지 최적화**: WebP 형식 사용

## API 개발

### 엔드포인트 설계
```python
# REST API 규칙
GET    /api/v1/pipelines           # 목록 조회
POST   /api/v1/pipelines           # 생성
GET    /api/v1/pipelines/{id}      # 단일 조회
PUT    /api/v1/pipelines/{id}      # 수정
DELETE /api/v1/pipelines/{id}      # 삭제
POST   /api/v1/pipelines/{id}/execute  # 실행
```

### 스키마 정의
```python
# Pydantic 스키마
class PipelineBase(BaseModel):
    name: str
    description: Optional[str] = None

class PipelineCreate(PipelineBase):
    config: Dict[str, Any]

class PipelineResponse(PipelineBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

## 데이터베이스

### 마이그레이션
```bash
# 새로운 마이그레이션 생성
alembic revision --autogenerate -m "Add pipeline table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 모델 정의
```python
# SQLAlchemy 모델
class Pipeline(Base):
    __tablename__ = "pipelines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## 배포

### Docker 빌드
```bash
# Backend 이미지 빌드
docker build -t toy-pipeline-backend ./backend

# Frontend 이미지 빌드
docker build -t toy-pipeline-frontend ./frontend

# 전체 스택 실행
docker-compose up -d
```

### 환경별 설정
- **Development**: `.env`
- **Staging**: `.env.staging`
- **Production**: `.env.production`

## 문제 해결

### 자주 발생하는 문제

1. **포트 충돌**
   ```bash
   # 포트 사용 확인
   lsof -i :8000
   lsof -i :3000
   ```

2. **데이터베이스 연결 오류**
   ```bash
   # PostgreSQL 상태 확인
   docker-compose ps postgres
   docker-compose logs postgres
   ```

3. **Redis 연결 오류**
   ```bash
   # Redis 상태 확인
   docker-compose exec redis redis-cli ping
   ```

4. **의존성 충돌**
   ```bash
   # 가상환경 재생성
   rm -rf venv
   python -m venv venv
   pip install -r requirements.txt
   ```

### 로그 확인
```bash
# 서비스별 로그 확인
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
docker-compose logs redis

# 실시간 로그 모니터링
docker-compose logs -f backend
```

## 유용한 명령어

### 개발 명령어
```bash
# 코드 포맷팅
cd backend && black . && isort .
cd frontend && npm run lint:fix

# 테스트 실행
cd backend && pytest
cd frontend && npm test

# 타입 체크
cd backend && mypy .
cd frontend && npm run type-check

# 의존성 업데이트
cd backend && pip-compile requirements.in
cd frontend && npm update
```

### 데이터베이스 관리
```bash
# 데이터베이스 초기화
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS toy_pipeline;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE toy_pipeline;"
alembic upgrade head

# 테스트 데이터 생성
python scripts/create_test_data.py
```

## 기여하기

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### PR 체크리스트
- [ ] 코드 리뷰 통과
- [ ] 테스트 작성 및 통과
- [ ] 문서 업데이트
- [ ] 타입 체크 통과
- [ ] 린트 통과
