--Запрос клиентов, удовлетворяющих правилам классификации Кэшбэк:
select c.clnt_id, sch.subs_subs_id, sh.rtpl_rtpl_id, seg.cseg_cseg_id, c.jrtp_jrtp_id
from clients c
left join client_histories ch on (ch.clnt_clnt_id=c.clnt_id and ch.start_date <= sysdate and ch.end_date > sysdate)
left join client_seg_histories seg on (seg.clnt_clnt_id = c.clnt_id and seg.cstp_cstp_id=1 and seg.start_date <= sysdate and seg.end_date > sysdate)
inner join subs_clnt_histories sch on (sch.clnt_clnt_id = c.clnt_id and sch.start_date <= sysdate and sch.end_date > sysdate and  sch.sbst_sbst_id =2) 
left join subs_histories sh on (sh.subs_subs_id = sch.subs_subs_id and sh.start_date <= sysdate and sh.end_date > sysdate)
where 
ch.clis_clis_id = 2 and 
c.jrtp_jrtp_id in (2, 3)
and sh.rtpl_rtpl_id in (157, 158, 159, 30)
and seg.cseg_cseg_id in (1, 2, 3, 4, 5, 8, 100) 
order by c.clnt_id;


-- Вывод лицевого счет
select *
  from cis_user_status_hist
 inner join client_histories
    on client_histories.clnt_clnt_id = cis_user_status_hist.subs_subs_id
 where cgro_cgro_id = 24
   and cis_user_status_hist.end_date > sysdate
   and cpst_cpst_id = 32
   and clnt_clnt_id in ( 69708, 70668, 70669)
   
select csh.cgro_cgro_id, csh.subs_subs_id, csh.cpst_cpst_id, csh.start_date, csh.end_date, csh.navi_date, cs.def, csh.navi_user 
from cis_user_status_hist csh, cis_statuses cs where cs.cpst_id=csh.cpst_cpst_id and csh.start_date <= sysdate and csh.end_date > sysdate and csh.cgro_cgro_id=3.


select *
  from cis_subs_all_phones_view
 where end_date > sysdate and subs_subs_id in (
                        select subs_subs_id
                          from cis_user_status_hist
                         inner join client_histories
                            on client_histories.clnt_clnt_id =
                               cis_user_status_hist.subs_subs_id
                         where cgro_cgro_id = 1
                           and cis_user_status_hist.end_date > sysdate
                           --and cpst_cpst_id = 7
                           )
						   
select * from BIS_VERSIONS t
join applications a
on t.appl_appl_id=a.appl_id and latest='Y'