import { describe, it, expect } from 'vitest'

// Моки утилитарных функций (как будто они существуют в проекте)
const formatDate = (date) => {
    return new Date(date).toLocaleDateString('ru-RU')
}

const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return regex.test(email)
}

const capitalizeString = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

const debounce = (func, delay) => {
    let timeoutId
    return (...args) => {
        clearTimeout(timeoutId)
        timeoutId = setTimeout(() => func.apply(null, args), delay)
    }
}

const generateId = () => {
    return Math.random().toString(36).substr(2, 9)
}

describe('Утилитарные функции', () => {
    describe('formatDate', () => {
        it('форматирует дату правильно', () => {
            const date = new Date('2024-01-15')
            const formatted = formatDate(date)
            expect(formatted).toMatch(/\d{2}\.\d{2}\.\d{4}/)
        })

        it('работает со строкой даты', () => {
            const result = formatDate('2024-12-25')
            expect(result).toBeTruthy()
            expect(typeof result).toBe('string')
        })
    })

    describe('validateEmail', () => {
        it('валидирует правильные email адреса', () => {
            expect(validateEmail('test@example.com')).toBe(true)
            expect(validateEmail('user.name+tag@domain.co.uk')).toBe(true)
        })

        it('отклоняет неправильные email адреса', () => {
            expect(validateEmail('invalid-email')).toBe(false)
            expect(validateEmail('test@')).toBe(false)
            expect(validateEmail('@domain.com')).toBe(false)
        })
    })

    describe('capitalizeString', () => {
        it('делает первую букву заглавной', () => {
            expect(capitalizeString('hello')).toBe('Hello')
            expect(capitalizeString('WORLD')).toBe('World')
        })

        it('обрабатывает пустые строки', () => {
            expect(capitalizeString('')).toBe('')
        })

        it('работает с одним символом', () => {
            expect(capitalizeString('a')).toBe('A')
        })
    })


    describe('generateId', () => {
        it('генерирует строку', () => {
            const id = generateId()
            expect(typeof id).toBe('string')
            expect(id.length).toBeGreaterThan(0)
        })

        it('генерирует уникальные ID', () => {
            const id1 = generateId()
            const id2 = generateId()
            expect(id1).not.toBe(id2)
        })

        it('генерирует ID правильной длины', () => {
            const id = generateId()
            expect(id.length).toBe(9)
        })
    })
})