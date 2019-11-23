//全选
        function ckAll(){
            var flag = document.getElementById("allChecks").checked;
            var cks = document.getElementsByName("input[]");
            for(var i=0;i<cks.length;i++){
                cks[i].checked=flag;
            }
        }
        //批量添加至检索结果页面
        function MultiAdd(){
            if(!confirm("确定添加这些吗?")){
                return;
            }
            var cks=document.getElementsByName("input[]");
            var str = "";
            //拼接所有的id
            for(var i=0;i<cks.length;i++){
                if(cks[i].checked){
                    str+=cks[i].value+",";
                }
            }
            //去掉字符串未尾的','
            str=str.substring(0, str.length-1);
            location.href='/search/searchlist/?ISBN='+str;
        }

        //从检索结果页面批量删除
        function MultiDel(){
            if(!confirm("确定删除这些记录吗?")){
                return;
            }
            var cks=document.getElementsByName("input[]");
            var str = "";
            //拼接所有的id
            for(var i=0;i<cks.length;i++){
                if(cks[i].checked){
                    str+=cks[i].value+",";
                }
            }
            //去掉字符串未尾的','
            str=str.substring(0, str.length-1);
            //此处的地址问题怎么处理？为什么仍旧为相对位置（相对于search）
            location.href='delete/?id='+str;
        }