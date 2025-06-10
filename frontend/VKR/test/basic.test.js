import { describe, it, expect } from 'vitest'

describe('Базовые тесты проекта', () => {
    it('математические операции работают корректно', () => {
        expect(2 + 2).toBe(4)
        expect(10 - 5).toBe(5)
        expect(3 * 4).toBe(12)
    })

    it('строки обрабатываются правильно', () => {
        const testString = 'Hello Nuxt.js'
        expect(testString).toContain('Nuxt')
        expect(testString.length).toBeGreaterThan(5)
        expect(testString.toLowerCase()).toBe('hello nuxt.js')
    })

    it('массивы работают как ожидается', () => {
        const testArray = [1, 2, 3, 4, 5]
        expect(testArray).toHaveLength(5)
        expect(testArray).toContain(3)
        expect(testArray[0]).toBe(1)
    })

    it('объекты создаются и изменяются', () => {
        const testObject = { name: 'Test', version: '1.0' }
        expect(testObject).toHaveProperty('name')
        expect(testObject.name).toBe('Test')

        testObject.description = 'Test description'
        expect(testObject).toHaveProperty('description')
    })

    it('Promise разрешается корректно', async () => {
        const testPromise = new Promise(resolve => {
            setTimeout(() => resolve('success'), 10)
        })

        const result = await testPromise
        expect(result).toBe('success')
    })
})