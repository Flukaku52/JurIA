import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Estendendo os matchers do Vitest com os do Jest DOM
expect.extend(matchers);

// Limpeza automática após cada teste
afterEach(() => {
  cleanup();
}); 