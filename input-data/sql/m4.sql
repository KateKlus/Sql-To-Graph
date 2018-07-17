select * from T1, (select * from T2, T3, T4 where T2.K > 0 and T3.K > 1 and T4.K > 2) where T3.K in (select T4.K from T4 where T4.K = 0);
