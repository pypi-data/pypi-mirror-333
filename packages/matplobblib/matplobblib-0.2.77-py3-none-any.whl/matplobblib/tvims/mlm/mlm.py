from ...forall import *
#######################################################################################################################
# Метод максимального правдоподобия
#######################################################################################################################
def mlm(text,splitter,bounds = [1,20]):
    """`Человек_1` и `Человек_2` исследуют эффективность лекарственного препарата АВС.
    `Человек_1`, используя модель `Человек_2`, создал компьютерную программу,
    вычисляющую по заданным генетическим факторам вероятность (в процентах) успешного применения АВС.
    Программа `Человек_1` накапливает полученные вероятности и в итоге выдает набор частот: n0,n1,...,n100.
    Например, n75 - это число случаев, в которых программа `Человек_1` получила вероятность 75%.
    Обработав `N` образцов генетического материала, `Человек_2` нашла значения факторов и ввела их в программу.
    В результате был получен следующий набор частот: `text`.
    Для завершения этапа исследования необходимо было подобрать распределение, соответствующее полученным частотам.
    Анна решила использовать распределение на отрезке [0,1] с плотностью 
    
    `f(x) = f(x;a,b) = a * b * x^(a - 1) * (1 - x^a)^(b - 1)`
    
    и целочисленными параметрами a,b в диапазоне от 1 до 20 [`bounds`].
    В результате максимизации функции правдоподобия (при указанных ограничениях)
    `Человек_1` были получены значения параметров: 
    a^ = A и b^ = B.
    Задача: пусть X - случайная величина, распределения на отрезке [0,1]
    с плотностью f(x)=f(x;a^,b^), F(x) - ее функция распределения.
    Требуется найти математическое ожидание E(X)
    и X_{0,2} = F^{−1} (0,2) - квантиль уровня 0,2.
    Какой смысл для всей популяции имеют E(X)и X_{0,2}?
    
    В ответе укажите:
    - значение A;
    - значение B;
    - математическое ожидание E(X);
    - квантиль X_{0,2}
    

    ## Args:
        text (str): Строка перечисления всех чисел, данных как `следующий набор частот`
        splitter (str): Разделитель между каждым значением в `text`
        bounds (list, optional): Границы, между которыми определены `a` и `b`. Стандартно равны = [1,20].
        
    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    ## Returns:
        `answer` (tuple): Соответствующие значения
    """
    import numpy as np
    from sympy import symbols,log, integrate
    from scipy import optimize

    nu = np.array([np.float64(i) for i in text.split(splitter)])

    x,n = symbols('x,n',integer=True, positive=True)
    a,b =symbols(r'\hat{a}, \hat{b}',integer=True, positive=True)

    f = a*b*x**(a-1)*(1-x**a)**(b-1)


    L = sum( [ i*log(f.subs({x:j})) for i,j in zip(nu,np.linspace (0,1,len(nu))) ] )

    chan = lambda soup:-L.subs({a:soup[0],b:soup[1]})
    out = optimize.minimize(chan,[int((bounds[1] - bounds[0])/2)+1,int((bounds[1] - bounds[0])/2)+1],bounds=(bounds,bounds))
    
    A,B = [round(_) for _ in out.x]
    print('Значение A = ' + str(A))
    print('Значение B = ' + str(B))

    E = integrate(x*f.subs({a:A,b:B}),(x,0,1))
    print(('Математическое ожидание = ' + one_rrstr(E.evalf(),3)))

    F = integrate(f.subs({a:A,b:B}),(x,0,x))
    shash = lambda cucumber: np.float64(F.subs({x:cucumber})-0.2)
    Q = optimize.root_scalar(shash,bracket=[0,1]).root
    print(('Квантиль = ' + one_rrstr(Q,3)))
    
    return (A,B,E.evalf(),Q)
#######################################################################################################################
MLM = [mlm]