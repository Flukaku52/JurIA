# JurIA Frontend

Este é o frontend da aplicação JurIA, uma plataforma de consultoria jurídica que utiliza inteligência artificial para responder a consultas jurídicas.

## Tecnologias Utilizadas

- React com TypeScript
- Vite para build e desenvolvimento
- Material UI para interface
- React Router para navegação
- React Hook Form para formulários
- Yup para validação
- Zustand para gerenciamento de estado
- Vitest e React Testing Library para testes

## Estrutura do Projeto

```
src/
├── components/       # Componentes reutilizáveis
├── contexts/         # Contextos React (AuthContext)
├── pages/            # Páginas da aplicação
├── services/         # Serviços para comunicação com a API
├── store/            # Stores Zustand para gerenciamento de estado
├── test/             # Configuração de testes
├── theme/            # Configuração do tema Material UI
├── types/            # Interfaces e tipos TypeScript
├── App.tsx           # Componente principal
└── main.tsx          # Ponto de entrada
```

## Melhorias Implementadas

### 1. Tipagem Aprimorada
- Utilizamos `import type` para importar tipos, melhorando a consistência do código
- Corrigimos tipagem em diversos componentes para maior segurança de tipo

### 2. Gerenciamento de Estado Global
- Implementamos Zustand para gerenciamento de estado global
- Criamos a store de consultas para gerenciar as consultas jurídicas

### 3. Testes Unitários
- Configuração do Vitest para executar testes
- Testes para o componente Navbar
- Configuração do Jest DOM para asserções de DOM

### 4. Otimização de Performance
- Utilizamos React.memo para evitar renderizações desnecessárias
- Implementamos useCallback e useMemo para memoização
- Refatoramos componentes para separar responsabilidades

## Como Executar

1. Instale as dependências:
```bash
npm install
```

2. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

3. Execute os testes:
```bash
npm test
```

## Próximos Passos

1. Expandir cobertura de testes
2. Adicionar testes de integração
3. Implementar cache para consultas frequentes
4. Implementar lazy loading para componentes grandes
5. Melhorar acessibilidade da aplicação

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
