---
applyTo: '**'
---

# Instruções do Projeto - NBA Trade Fit Simulator

## Contexto
**NBA Trade Fit Simulator** é uma aplicação full-stack para simular o encaixe de jogadores da NBA em times específicos. Analisa estatísticas de jogadores, identifica arquétipos, detecta lacunas do time e calcula um "Fit Score" usando algoritmos de Data Science com Pandas.

**Status**: ��� Em desenvolvimento ativo (Dezembro 2025)

## Regras Críticas

### ��� Prioridade Máxima
- **NUNCA** remova código de produção sem validação completa dos impactos
- **NUNCA** rode comandos `sleep` ou similares para aguardar processos - sempre use comandos em background e obtenha output via get_terminal_output
- **NUNCA** interrompa processos em background com Ctrl+C
- **SEMPRE** receba output de terminais background aqui no chat usando get_terminal_output
- **SEMPRE** aguarde processos de build/compilação terminarem naturalmente
- **NUNCA** use `any` em código TypeScript novo - sempre defina interfaces/tipos
- **NUNCA** use `# type: ignore` em Python sem justificativa
- **SEMPRE** use Pydantic models para validação de dados na API
- **SEMPRE** trate erros de API externa (nba_api pode falhar)
- **SEMPRE** use async/await para endpoints FastAPI
- **SEMPRE** destrua Subscriptions Angular (unsubscribe, takeUntilDestroyed, async pipe)

### Compatibilidade
- Backend: Python 3.11+ (sem suporte a versões anteriores)
- Frontend: Angular 17.3+ (Standalone Components obrigatório)
- Node: 18.16+ (compatível com Angular 17)

### Qualidade de Código
- Priorize legibilidade sobre cleverness
- Código auto-explicativo > comentários extensos
- DRY: Evite duplicação entre services

## Communication Style
- **Seja direto e objetivo** - vá direto ao ponto técnico
- **Evite verbosidade** - respostas concisas mas completas
- **Mostre código, não descreva** - prefira exemplos práticos
- **Destaque riscos** - alerte sobre breaking changes ou impactos críticos

---

## Stack Técnica

### Backend (Python)
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.104+ | Framework REST API |
| **Uvicorn** | 0.24+ | ASGI Server |
| **Pydantic** | 2.5+ | Validação e schemas |
| **Pandas** | 2.1+ | Análise de dados |
| **NumPy** | 1.26+ | Operações numéricas |
| **SQLAlchemy** | 2.0+ | ORM (futuro) |
| **nba_api** | 1.4+ | Dados oficiais NBA |
| **pytest** | 7.4+ | Testes unitários |

### Frontend (Angular)
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Angular** | 17.3+ | Framework UI |
| **Angular Material** | 17.3+ | Componentes UI |
| **RxJS** | 7.8+ | Programação reativa |
| **TypeScript** | 5.4+ | Linguagem |
| **ngx-charts** | 20.5+ | Visualização de dados |

---

## Arquitetura do Projeto

### Estrutura de Pastas
```
nba-trade-fit-simulator/
├── .github/
│   └── copilot-instructions.md   # Este arquivo
│
├── backend/
│   ├── src/
│   │   ├── main.py               # Entry point FastAPI
│   │   ├── api/
│   │   │   ├── dependencies.py   # Injeção de dependências
│   │   │   └── routes/
│   │   │       └── simulation.py # Endpoints de simulação
│   │   ├── core/
│   │   │   ├── config.py         # Configurações (env vars)
│   │   │   └── constants.py      # Constantes do domínio
│   │   ├── domain/
│   │   │   ├── entities/         # Entidades de domínio
│   │   │   │   ├── player.py
│   │   │   │   └── team.py
│   │   │   └── services/         # Lógica de negócio
│   │   │       ├── fit_simulator.py           # Orquestrador principal
│   │   │       ├── player_archetype_service.py # Análise de arquétipos
│   │   │       ├── team_gap_service.py        # Análise de lacunas
│   │   │       └── roster_friction_service.py # Análise de conflitos
│   │   ├── infrastructure/
│   │   │   ├── database/         # SQLAlchemy models
│   │   │   └── external/
│   │   │       └── nba_api_client.py  # Cliente NBA API
│   │   └── schemas/              # Pydantic models
│   │       ├── analysis.py       # Schemas de análise (core)
│   │       ├── player.py
│   │       ├── team.py
│   │       └── simulation.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_simulation.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts      # Root component
│   │   │   ├── app.config.ts         # App configuration
│   │   │   ├── app.routes.ts         # Rotas
│   │   │   ├── core/
│   │   │   │   ├── interceptors/     # HTTP interceptors
│   │   │   │   ├── models/           # Interfaces TypeScript
│   │   │   │   └── services/         # Services HTTP
│   │   │   ├── features/
│   │   │   │   └── simulator/        # Feature principal
│   │   │   │       ├── components/   # Sub-componentes
│   │   │   │       └── simulator.component.ts
│   │   │   └── shared/
│   │   │       └── components/       # Componentes reutilizáveis
│   │   └── environments/
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
└── README.md
```

---

## Padrões de Código

### Backend (Python)

#### Convenções de Nomenclatura
```python
# Classes: PascalCase
class FitSimulator:
class PlayerArchetypeService:

# Funções e métodos: snake_case
def calculate_fit_score():
async def simulate_fit():

# Variáveis: snake_case
player_stats = ...
fit_score = 0

# Constantes: UPPER_SNAKE_CASE
MAX_PENALTY_POINTS = 100
DEFAULT_FIT_SCORE = 75

# Pydantic Models: PascalCase
class PlayerAdvancedStats(BaseModel):
class TradeResult(BaseModel):

# Enums: PascalCase com valores string
class FitLabel(str, Enum):
    PERFECT_FIT = "Perfect Fit"
    BAD_FIT = "Bad Fit"
```

#### Estrutura de Arquivos Python
```python
# service.py - Estrutura padrão
from typing import Optional, List
from src.schemas.analysis import PlayerAnalysis, TeamStats

class MyService:
    """
    Docstring descrevendo responsabilidade do serviço.
    """

    def __init__(self, dependency: Optional[OtherService] = None):
        self.dependency = dependency or OtherService()

    def public_method(self, param: int) -> Result:
        """Docstring para métodos públicos."""
        return self._private_helper(param)

    def _private_helper(self, param: int) -> Result:
        # Métodos privados com underscore
        pass
```

#### Pydantic Schemas
```python
# ✅ BOM - Schema bem definido
class PlayerAdvancedStats(BaseModel):
    player_id: int
    player_name: str
    pts: float = Field(default=0.0, description="Pontos por jogo")
    fg3_pct: float = Field(default=0.0, ge=0.0, le=1.0)
    
    model_config = ConfigDict(
        json_schema_extra={"example": {"player_id": 123, "player_name": "LeBron"}}
    )

# ❌ RUIM - Sem tipagem ou validação
class PlayerStats:
    def __init__(self, data):
        self.data = data  # ⚠️ Sem validação!
```

#### Tratamento de Erros
```python
# ✅ BOM - Tratamento explícito
async def get_player_stats(player_id: int) -> Optional[PlayerAdvancedStats]:
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(...)
        df = stats.get_data_frames()[0]
        # processar...
        return PlayerAdvancedStats(...)
    except Exception as e:
        print(f"[NBAApiClient] Erro ao buscar stats {player_id}: {e}")
        return None  # Retorna None, não quebra a aplicação

# ❌ RUIM - Deixa exception vazar
async def get_player_stats(player_id: int):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(...)  # ⚠️ Pode quebrar!
    return stats
```

### Frontend (Angular)

#### Convenções de Nomenclatura
```typescript
// Componentes: PascalCase + Component suffix
export class SimulatorComponent {}
export class PlayerSearchComponent {}

// Services: PascalCase + Service suffix
export class SimulationService {}

// Interfaces: PascalCase com prefixo I
export interface IPlayer {}
export interface ISimulationResult {}

// Observables: $ suffix
players$ = this.http.get<IPlayer[]>('/players');
loading$ = new BehaviorSubject<boolean>(false);

// Signals: sem suffix especial (Angular 17+)
count = signal(0);
doubleCount = computed(() => this.count() * 2);
```

#### Standalone Components (OBRIGATÓRIO em Angular 17)
```typescript
// ✅ BOM - Standalone component
@Component({
  selector: 'app-player-search',
  standalone: true,
  imports: [
    CommonModule,
    MatInputModule,
    MatAutocompleteModule,
    ReactiveFormsModule
  ],
  templateUrl: './player-search.component.html'
})
export class PlayerSearchComponent {
  private destroyRef = inject(DestroyRef);
  
  ngOnInit() {
    this.someObservable$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe();
  }
}

// ❌ EVITAR - NgModule-based (legado)
@NgModule({
  declarations: [PlayerSearchComponent],
  imports: [...]
})
export class PlayerModule {}
```

#### HTTP Calls
```typescript
// ✅ BOM - Service com tipagem forte
@Injectable({ providedIn: 'root' })
export class SimulationService {
  private readonly API_URL = 'http://localhost:8000/api/v1';
  private http = inject(HttpClient);

  simulateFit(playerId: number, teamId: number): Observable<ISimulationResult> {
    const params = new HttpParams()
      .set('player_id', playerId)
      .set('team_id', teamId);
      
    return this.http.get<ISimulationResult>(
      `${this.API_URL}/simulate-fit`,
      { params }
    ).pipe(
      catchError(error => {
        console.error('[SimulationService] Erro:', error);
        return throwError(() => error);
      })
    );
  }
}
```

#### Gerenciamento de Subscriptions
```typescript
// ✅ OPÇÃO 1: takeUntilDestroyed (Angular 17+ - PREFERIDO)
export class MyComponent {
  private destroyRef = inject(DestroyRef);
  
  ngOnInit() {
    this.data$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(data => this.handleData(data));
  }
}

// ✅ OPÇÃO 2: async pipe (melhor para templates)
@Component({
  template: `
    @if (result$ | async; as result) {
      <app-result-display [result]="result" />
    }
  `
})
export class MyComponent {
  result$ = this.service.getData();
}

// ❌ RUIM - Memory leak!
ngOnInit() {
  this.data$.subscribe(data => this.data = data); // ⚠️ Nunca faz unsubscribe!
}
```

---

## Domínio de Negócio - Sporting Fit Algorithm

### Arquétipos de Jogadores
O sistema classifica jogadores em arquétipos baseado em estatísticas:

| Arquétipo | Critério |
|-----------|----------|
| **Sniper** | 3PA > 5.0 e 3P% > 37% |
| **Ball Dominant** | USG% > 25% |
| **Playmaker** | AST > 6.0 ou AST% > 25% |
| **Rim Protector** | BLK > 1.5 |
| **Hustle** | REB > 8.0 ou OREB > 2.5 |
| **3&D** | 3P% > 36% e (STL > 1.0 ou BLK > 0.8) |
| **Stretch Big** | Posição C/PF e 3P% > 35% |

### Lacunas do Time (Team Gaps)
Identificadas quando time está no bottom 10 de ranking:

| Ranking > 20 | Necessidade Gerada |
|--------------|-------------------|
| FG3% Rank | Shooting |
| REB Rank | Rebounding |
| AST Rank | Playmaking |
| DEF Rating | Rim Protection + Perimeter Defense |
| OFF Rating | Scoring |

### Fricção no Elenco (Roster Friction)
Penalidades aplicadas ao Fit Score:

| Conflito | Penalidade |
|----------|-----------|
| Ball Dominant + Time com 2+ Ball Dominants | -30 pts |
| Ball Dominant + Time com 1 Ball Dominant | -15 pts |
| Pivô pesado + Time top 5 em Pace | -20 pts |

### Cálculo do Fit Score
```python
BASE_SCORE = 75

# Bônus por atender necessidades
if need == "Shooting" and archetype in ["Sniper", "Stretch Big"]:
    score += 15
if need == "Rim Protection" and archetype == "Rim Protector":
    score += 15
if need == "Playmaking" and archetype == "Playmaker":
    score += 15

# Penalidade por fricção
score -= friction.total_penalty

# Labels finais
90-100: Perfect Fit
80-89:  Starter
60-79:  Rotation Player
40-59:  Situational
0-39:   Bad Fit
```

---

## Ao Fazer Mudanças

### SEMPRE
- ✅ Ler o arquivo **completo** antes de modificar
- ✅ Verificar todos os **imports** e dependências
- ✅ Manter formatação e estilo existentes
- ✅ Adicionar docstrings em classes/funções públicas
- ✅ Validar tipos (Pydantic no backend, interfaces no frontend)
- ✅ Tratar erros de API externa (nba_api pode falhar)
- ✅ Usar `grep_search` para verificar usages antes de modificar
- ✅ Testar manualmente após mudanças em services

### NUNCA
- ❌ Assumir estrutura sem verificar com `read_file`
- ❌ Usar `any` (TypeScript) ou `# type: ignore` (Python) sem justificativa
- ❌ Ignorar error handling em chamadas à nba_api
- ❌ Fazer subscribe sem cleanup (Angular)
- ❌ Hardcodar URLs de API
- ❌ Remover código "aparentemente não usado" sem buscar usages

---

## Comandos de Desenvolvimento

### Backend
```bash
# Navegar para pasta
cd backend

# Ativar venv (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor (development)
uvicorn src.main:app --reload --port 8000

# Rodar testes
pytest

# Rodar testes com coverage
pytest --cov=src
```

### Frontend
```bash
# Navegar para pasta
cd frontend

# Instalar dependências
npm install

# Rodar servidor (development)
ng serve
# ou
npm start

# Build produção
ng build --configuration production

# Rodar testes
ng test
```

### Acessos
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Tratamento de Erros

### Backend
```python
# Em routes/simulation.py
@router.get("/simulate-fit", response_model=SimulationResponse)
async def simulate_fit(
    player_id: int = Query(...),
    team_id: int = Query(...)
):
    try:
        result = await fit_simulator.simulate_fit(player_id, team_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar simulação: {str(e)}"
        )
```

### Frontend
```typescript
// Em components
this.simulationService.simulateFit(playerId, teamId).pipe(
  catchError(error => {
    this.snackBar.open('Erro ao simular. Tente novamente.', 'Fechar');
    return EMPTY;
  }),
  takeUntilDestroyed(this.destroyRef)
).subscribe(result => {
  this.result = result;
});
```

---

## Testes

### Backend (pytest)
```python
# tests/test_simulation.py
import pytest
from src.domain.services.player_archetype_service import PlayerArchetypeService
from src.schemas.analysis import PlayerAdvancedStats, PlayerArchetype

def test_sniper_archetype():
    """Jogador com 3PA > 5 e 3P% > 37% deve ser Sniper"""
    service = PlayerArchetypeService()
    stats = PlayerAdvancedStats(
        player_id=1,
        player_name="Test Player",
        fg3a=6.0,
        fg3_pct=0.40
    )
    
    analysis = service.analyze_player(stats)
    
    assert PlayerArchetype.SNIPER in analysis.archetypes
```

### Frontend (Jest/Karma)
```typescript
// simulation.service.spec.ts
describe('SimulationService', () => {
  let service: SimulationService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SimulationService]
    });
    service = TestBed.inject(SimulationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should call simulate-fit endpoint', () => {
    service.simulateFit(123, 456).subscribe();
    
    const req = httpMock.expectOne(r => r.url.includes('simulate-fit'));
    expect(req.request.params.get('player_id')).toBe('123');
  });
});
```

---

## Troubleshooting

### Problema: nba_api retorna dados vazios
**Causa**: Temporada não iniciou ou jogador não tem stats
**Solução**: Fazer fallback para temporada anterior
```python
if player_row.empty:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2023-24")
```

### Problema: CORS error no frontend
**Causa**: Backend não configurou CORS
**Solução**: Verificar `main.py` tem CORSMiddleware
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problema: Import circular no backend
**Causa**: Services importando uns aos outros
**Solução**: Usar injeção via `__init__` ou mover para arquivo separado

### Problema: Angular Material icons não aparecem
**Causa**: Falta link do Material Icons no `index.html`
**Solução**: Adicionar no `<head>`:
```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

---

## ��� Quick Start

```bash
# 1. Clonar repositório
git clone <repo>
cd nba-trade-fit-simulator

# 2. Setup Backend
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn src.main:app --reload

# 3. Setup Frontend (outro terminal)
cd frontend
npm install
ng serve

# 4. Acessar
# Frontend: http://localhost:4200
# API Docs: http://localhost:8000/docs
```

---

## ��� Checklist de PR

- [ ] Código compila sem erros
- [ ] Testes passam: `pytest` (backend) e `ng test` (frontend)
- [ ] Sem `any` em TypeScript novo
- [ ] Pydantic models para novos endpoints
- [ ] Error handling em chamadas à nba_api
- [ ] Subscriptions Angular têm cleanup
- [ ] Docstrings em funções públicas
- [ ] README atualizado se necessário

---

## ��� Roadmap

### MVP (Atual)
- ✅ Busca de jogadores por nome
- ✅ Seleção de time alvo
- ✅ Algoritmo de Sporting Fit (Archetypes + Gaps + Friction)
- ✅ Exibição de resultado com score e reasons

### v1.0 (Próximo)
- ��� Gráficos de breakdown do score (ngx-charts)
- ��� Comparação side-by-side de múltiplos trades
- ��� Histórico de simulações (SQLite)
- ��� Cache de dados da NBA API

### v2.0 (Futuro)
- ��� Multi-player trades
- ��� Salary cap analysis
- ��� Draft pick simulation
- ��� Deploy em cloud (Azure/AWS)

---

**Última Atualização**: 4 de Dezembro de 2025

**Nota**: Este arquivo é lido pelo Copilot em toda interação. Mantenha atualizado com padrões e decisões do projeto.
