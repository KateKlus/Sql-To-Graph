select * from T1 where T1.K > 0 order by T1.K union (select T2.K, T3.K from T2, T3 where T2.K > 0 order by T2.K) union (select T4.K from T4 where T4.K > 0 order by T4.K);
