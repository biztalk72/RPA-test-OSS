# 통합 워크플로우 테스트 문서

## 개요

이 테스트는 실제 RPA 시나리오를 모방하여 다음 세 가지 자동화 유형을 순차적으로 실행합니다:

1. **Native Application 자동화** (macOS Notes 앱)
2. **웹 스크래핑** (quotes.toscrape.com)
3. **Excel 다중 시트 통합**

## 테스트 시나리오

### Test 1: Native Application 자동화

#### 목적
macOS 기본 앱(Notes)을 자동으로 제어하여 RPA가 데스크톱 애플리케이션과 상호작용할 수 있는지 검증

#### 단계
1. Notes 앱 실행
2. 새 노트 생성
   - 제목: "RPA Test Note"
   - 내용: 테스트 실행 시간, 상태, 프레임워크 정보
3. 노트 수 확인 (검증)
4. Notes 앱 종료

#### 기술 구현
- **AppleScript**: macOS 앱 제어
- **subprocess**: Python에서 시스템 명령 실행
- **시간 지연**: 앱 실행 대기

#### 예상 결과
```
✓ Note created successfully (Total notes: X)
✓ Native app automation completed successfully!
```

### Test 2: 웹 스크래핑

#### 목적
공개 웹사이트에서 구조화된 데이터를 추출하는 능력 검증

#### 대상 사이트
- **URL**: https://quotes.toscrape.com/
- **이유**: 
  - 테스트 전용 공개 사이트
  - 안정적인 HTML 구조
  - 인증 불필요
  - robots.txt 허용

#### 추출 데이터
- 명언 텍스트 (Quote)
- 작가 이름 (Author)
- 태그 (Tags)
- 5개 항목 수집

#### 기술 구현
- **requests**: HTTP 요청
- **BeautifulSoup4**: HTML 파싱
- **CSS 선택자**: 요소 찾기

#### 예상 결과
```
✓ Successfully scraped 5 quotes
  1. Albert Einstein: "The world as we have created it..."
  2. J.K. Rowling: "It is our choices, Harry..."
  ...
```

### Test 3: Excel 다중 시트 통합

#### 목적
수집된 다양한 데이터를 Excel 파일의 여러 시트에 통합하여 보고서 생성

#### 생성 시트

##### Sheet 1: "Calculations"
비즈니스 데이터 및 계산식
- 제품명, 수량, 가격
- 수식: `=수량 * 가격`
- 합계: `=SUM()`

**샘플 데이터:**
| Item | Quantity | Price | Total |
|------|----------|-------|-------|
| Product A | 10 | 25.50 | =B2*C2 |
| Product B | 5 | 42.00 | =B3*C3 |
| ... | ... | ... | ... |
| **TOTAL** | | | =SUM(D2:D6) |

##### Sheet 2: "Web Quotes"
웹 스크래핑 결과
- 번호, 명언, 작가, 태그, 수집 시간

**데이터 출처**: Test 2의 웹 스크래핑 결과

##### Sheet 3: "Dashboard"
테스트 요약 대시보드
- 테스트 실행 정보
- 각 테스트 통과/실패 상태
- 데이터 요약 (제품 수, 총 매출, 명언 수)
- 시트 간 참조 수식

**예시:**
```
RPA Integration Test Dashboard
Test Date: 2024-12-24 14:30:15

Test Results:
1. Native App Automation    ✓ Passed
2. Web Scraping              ✓ Passed (5 quotes)
3. Excel Integration         ✓ Passed

Data Summary:
Total Products:    =COUNTA(Calculations!A2:A6)
Total Revenue:     =Calculations!D7
Quotes Collected:  5
```

#### 기술 구현
- **openpyxl**: Excel 파일 생성 및 조작
- **다중 시트 관리**: create_sheet()
- **수식 작성**: Excel 네이티브 수식
- **시트 간 참조**: `SheetName!Cell` 문법

#### 검증
1. 파일 생성 확인
2. 3개 시트 존재 확인
3. 시트 이름 검증

## 실행 방법

### 개별 실행
```bash
cd /Users/sy2024051047/RPA-test-OSS
source venv/bin/activate
python3 implementations/rpa-python/integrated_test.py
```

### 벤치마크 실행 (10회 반복)
```bash
python3 test_runner.py
```

## 성능 메트릭

### 실측 결과
- **총 실행 시간**: ~9초
- **테스트 1 (Native App)**: ~3초
- **테스트 2 (Web Scraping)**: ~2초
- **테스트 3 (Excel)**: ~4초

### 리소스 사용
- **메모리**: 최소 (웹 요청 시 일시적 증가)
- **CPU**: 중간 (앱 실행 및 HTML 파싱)
- **네트워크**: 1회 HTTP GET 요청

## 출력 파일

### 위치
```
/Users/sy2024051047/RPA-test-OSS/test-data/excel/integrated_test_output.xlsx
```

### 구조
```
integrated_test_output.xlsx
├── Calculations (Sheet1)
│   └── 5개 제품 + 수식 + 합계
├── Web Quotes (Sheet2)
│   └── 5개 명언 + 메타데이터
└── Dashboard (Sheet3)
    └── 테스트 요약 + 통계
```

### Excel에서 확인
```bash
open test-data/excel/integrated_test_output.xlsx
```

## 오류 처리

### Notes 앱 권한
macOS는 처음 실행 시 Notes 접근 권한을 요청할 수 있습니다.
- **해결**: 시스템 설정 > 개인 정보 보호 > 자동화에서 Terminal/IDE에 Notes 권한 부여

### 웹 스크래핑 실패
네트워크 연결 문제나 사이트 다운타임
- **처리**: 예외 처리로 빈 배열 반환, Excel 테스트 건너뛰기
- **재시도**: 테스트 재실행

### AppleScript 오류
macOS 보안 설정으로 인한 실행 제한
- **해결**: 시스템 설정에서 앱 권한 확인

## 실제 사용 사례

이 통합 테스트는 다음과 같은 실제 RPA 시나리오를 시뮬레이션합니다:

### 사례 1: 일일 보고서 자동화
1. 이메일 클라이언트에서 특정 메일 읽기 (Native App)
2. 회사 인트라넷에서 데이터 수집 (Web Scraping)
3. Excel 보고서 생성 및 배포 (Excel Integration)

### 사례 2: 경쟁사 가격 모니터링
1. 알림 앱에 모니터링 기록 (Native App)
2. 경쟁사 웹사이트 가격 수집 (Web Scraping)
3. 비교 분석 스프레드시트 생성 (Excel Integration)

### 사례 3: 데이터 수집 및 분석
1. 로컬 앱에서 데이터 추출 (Native App)
2. API 또는 웹에서 추가 데이터 (Web Scraping)
3. 통합 분석 리포트 (Excel Integration)

## 확장 가능성

### 추가 가능한 테스트
1. **이메일 자동화**: Notes 대신 Mail.app 사용
2. **다중 페이지 스크래핑**: 페이지네이션 처리
3. **데이터베이스 통합**: SQLite 또는 PostgreSQL
4. **API 호출**: REST API 통합
5. **파일 처리**: PDF 생성, 이미지 처리
6. **알림**: Slack, 이메일 알림 전송

### 성능 최적화
1. **병렬 처리**: 독립적인 작업 동시 실행
2. **캐싱**: 웹 요청 결과 캐시
3. **비동기 처리**: asyncio 활용
4. **리소스 풀링**: 연결 재사용

## 비교 분석

### RPA Python의 강점 (본 테스트 기준)
1. ✅ **유연성**: 모든 자동화 타입을 하나의 스크립트로
2. ✅ **통합성**: 서로 다른 데이터 소스 쉽게 결합
3. ✅ **제어력**: 세밀한 오류 처리 및 로직
4. ✅ **확장성**: 라이브러리 추가로 기능 확장
5. ✅ **디버깅**: 각 단계별 상세 로깅

### 다른 프레임워크와의 비교
| 특성 | RPA Python | Robot Framework | TagUI |
|-----|-----------|----------------|-------|
| 통합 테스트 난이도 | 쉬움 | 보통 | 어려움 |
| 코드 복잡도 | 중간 | 높음 | 낮음 (기능 제한적) |
| 실행 속도 | 빠름 | 느림 | 빠름 |
| 디버깅 | 용이 | 보통 | 어려움 |

## 결론

이 통합 테스트는 RPA Python이 다음을 수행할 수 있음을 입증합니다:

1. ✅ Native macOS 애플리케이션 제어
2. ✅ 웹 데이터 수집 및 파싱
3. ✅ 복잡한 Excel 파일 생성 (다중 시트, 수식)
4. ✅ 여러 데이터 소스 통합
5. ✅ 안정적인 오류 처리
6. ✅ 실제 업무 시나리오 시뮬레이션

**성공률**: 100%  
**평균 실행 시간**: 9.01초  
**안정성**: 우수

---

**작성일**: 2024년 12월  
**테스트 환경**: macOS Apple Silicon  
**프로젝트**: RPA-test-OSS
