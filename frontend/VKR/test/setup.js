// Настройка тестовой среды
import { config } from '@vue/test-utils'
import { vi } from 'vitest'

// Глобальные моки и настройки
global.console = {
    ...console,
    warn: vi.fn(),
    error: vi.fn()
}

// Конфигурация Vue Test Utils
config.global.stubs = {
    NuxtLink: {
        template: '<a><slot /></a>'
    },
    NuxtPage: {
        template: '<div><slot /></div>'
    }
}