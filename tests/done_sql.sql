select * from T1 where T1.K > 0 order by T1.K;
select T1.K, T2.K from T1, T2 where T1.K > 0 order by T1.K;
select * from T1 where T1.K in (select T2.K from T2 where T2.K in (select T3.K from T3 where T3.K in (select T4.K from T4 where T4.K = 0 ))) order by T1.K;
select * from T1, (select * from T2, T3, T4 where T2.K > 0 and T3.K > 1 and T4.K > 2) where T1.K > 0;