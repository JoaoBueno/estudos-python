

times = lambda x, y: x * y
times2 = lambda x: times(x, 2)
isEqual = lambda x, y: x == y
isNotEqual = lambda x, y: not(isEqual(x, y))
generateSum = times
toSums = lambda qtd: lambda [sum2, sum1], n: [sum2 + generateSum(n, qtd), sum1 + generateSum(n, --qtd)]
# const toSums = total => ([sum2, sum1], n) => [sum2 + generateSum(n)(total), sum1 + generateSum(n)(--total)]
getSums = lambda x, qtd = 11: x.split('').slice(0, 9).reduce(toSums(qtd, 0, 0).reverse()

# mod11 = lambda x: x % 11


print(toSums(11, 0, 0 ))
print(times(2, 2))
print(times2(2))
print(isEqual(123, 123))
print(isEqual(2, 3))
print(isNotEqual(123, 123))
print(isNotEqual(2, 3))

print(toSums(11, 0, 0, 0))

# const NOT = a => !a
# const times = a => b => b * a
# const mod11 = num => num % 11
# const times2 = num => times(2)(num)
# const times10 = num => times(10)(num)
# const isEqual = a => b => b === a
# const isNotEqual = a => b => !isEqual(a)(b)
# const getDigit = cpf => `${cpf.charAt(9)}${cpf.charAt(10)}`
# const getGeneratedDigit = (sum1, sum2) => (sum1 === 0 ? '0' + sum2 : sum1 * 10 + sum2 + '')
# const generateStringSequence = tam => num => `${num}`.repeat(tam)
# const generateArray = length => Array.from({ length }, (v, k) => k)
# const generateSum = times
# const generateSequenceSize11 = generateStringSequence(11)
# const inSameDigits = cpf => num => isEqual(cpf)(generateSequenceSize11(num))
# const isIn = list => value => list.findIndex(inSameDigits(value)) >= 0
# const testIfHasSameDigits = list => cpf => isIn(list)(cpf)
# const getResultOfSum1 = sum1 => (mod11(sum1) < 2 ? 0 : 11 - mod11(sum1)) // 11 - mod11(  sum1 )
# const getResultOfSum2 = (
#   sum1,
#   sum2 // 11 - mod11( sum2 + times2( sum1 ) )
# ) => (mod11(sum2 + times2(sum1)) < 2 ? 0 : 11 - mod11(sum2 + times2(sum1)))

# const toSums = total => ([sum2, sum1], n) => [sum2 + generateSum(n)(total), sum1 + generateSum(n)(--total)]

# const getSums = (cpf, total = 11) => cpf.split('').slice(0, 9).reduce(toSums(total), [0, 0]).reverse()

# const validate = cpf => {
#   const CPF_LENGTH = 11
#   let [sum1, sum2] = getSums(cpf, CPF_LENGTH)

#   sum1 = getResultOfSum1(sum1)
#   sum2 = getResultOfSum2(sum1, sum2)

#   return NOT(testIfHasSameDigits(generateArray(10))(cpf)) && NOT(getGeneratedDigit(sum1, sum2) !== getDigit(cpf))
# }

# const CPFS = ['04998264931', '03506838326', '04864713901', '03506838321', '22222222222', '00000000000', '07468287805']

# CPFS.forEach(cpf => console.log(`${cpf}: ${validate(cpf)}`))

# module.exports = validate

