// 先注册需要进行ajax的链接的点击函数，然后在执行ajax的函数中重新注册
    $(document).ready(
      function() { 

        function displayComment(container) {
          var el = document.getElementById("ds-thread");
          DUOSHUO.EmbedThread(el);
          container.html(el);
        };

        // create a pagedown converter - regular and sanitized versions are both supported 
        var converter = new Markdown.Converter();
        // tell the converter to use Markdown Extra
        Markdown.Extra.init(converter, {
          extensions: "all",
          highlighter: "prettify"
        });

        var chopScriptTag = function (str) {
          var index = str.lastIndexof('<script type="text/javascript">');
          return str.substr(0, index-1);
        }
        var convertMD2Html = function (content) {
          return converter.makeHtml(content);
        }
        // prettify the content
        var callPrettify = function () {
          prettyPrint();
        }

        var init_Scroll = function(){
          $("#m-sidebar").niceScroll();
          $("#m-post-list").niceScroll();
        }
        init_Scroll();

        //set the active class 
        (function set_active_class(){
          $(".m-class-collapse li").each(function(){
            $(this).click(function(event){
              $(".current-selected-class").removeClass("current-selected-class");
              $(this).addClass("current-selected-class");
            });
          });
        })();

        // set the animation of the list
        $("#m-post-list > article").animo({animation: "fadeInLeft", duration: 0.4, keep: true});

        function setArticleToPage (data) {
          container=$("#post");
          // markdown to html
          container.html(convertMD2Html(data));
          // update the comment after display the article
          displayComment($("#comment-box"));

          $("#post").animo({animation: "fadeInUp", 
            duration: 0.6,keep: true});
        }

        (function convertContent () {
            var container = $("#main-content");
            container.html(convertMD2Html(container.text()));
            $("#post").animo({animation: "fadeInUp", 
              duration: 0.6,keep: true});
            callPrettify();
        })();
        // load the first article
        // $.get($(".post-link:first").attr("href"),function(data){
        //   setArticleToPage(data);
        //   callPrettify();
        // },'html');
        

        var artitle_ajax_load  = function(url) {
          $("#post").animo({animation: "fadeOutDown", duration: 0.6, keep: true},function() {
            //ajax get the article
            $.get(url,function(data){
                setArticleToPage(data);
                callPrettify();
              },'html');
          });
        }

        var article_list_ajax_load = function(url){
          var selector = "#m-list-post-";
          var setFadeOutRight = function(index,sum){
            if(index <= sum){
              var child = selector + index;
              $(child).animo({animation: "fadeOutRight", duration: 0.1, keep: true},function(){
                setFadeOutRight(index+1, sum);
              });
            }else{
              //ajax get the article list
              $.get(url,function(data){
                container=$("#m-post-list");
                container.html(data);
                var setFadeInLeft = function(index,sum){
                  //traverse the m-list-post
                  if(index <= sum){
                    var child = selector + index;
                    $(child).animo({animation: "fadeInLeft", duration: 0.1, keep: true},function(){
                      setFadeInLeft(index+1, sum);
                    });
                  }
                }
                // the pager is the last child of the post-list
                setFadeInLeft(1,$("#m-post-list").children().length-1);
                bind_article_ajax();
                bind_pager_ajax();
              });
            }
          }//end setFadeOutRight
          setFadeOutRight(1,$("#m-post-list").children().length-1);
        }// end article_list_ajax_load

        var bind_article_list_ajax = function(){
          $(".class-link").each(function(){
            $(this).click(function(event){
              event.preventDefault();
              var uri = $(this).attr("href");
              var newtitle = $(this).text();
              article_list_ajax_load(uri);
              
              if(history.pushState){
                //pushState
                document.title = newtitle;
                var state = {
                  url: uri, title: newtitle, type: "article_list"
                }
                history.pushState(state, newtitle, uri);
              }
            })
          });
        }

        var bind_article_ajax = function(){
          $(".post-link").each(function(){
            $(this).click(function(event) {
              event.preventDefault();
              var newtitle = $(this).text();
              var uri = $(this).attr("href");
              artitle_ajax_load(uri);

              if(history.pushState){
                //pushState
                document.title = newtitle;
                var state = {
                  url: uri, title: newtitle, type: "article"
                }
                history.pushState(state, newtitle, uri);
              }
              $(".current-selected-post").removeClass("current-selected-post");
              $(this).parents("article").addClass("current-selected-post");
            });
          });
        }

        if (history.pushState) {
            window.addEventListener("popstate", function(event) {
                var state = event.state;
                var newtitle = state.title;
                document.title = newtitle;
                switch(state.type){
                  case "article_list":
                    console.log("article_list");
                    console.log(state.url);
                    article_list_ajax_load(state.url);
                    break;
                  case "article":
                    console.log("article");
                    console.log(state.url);
                    artitle_ajax_load(state.url);
                    break;
                }
            });
        }
        var bind_pager_ajax = function(){
          $('#m-previous').click(function(event){
            event.preventDefault();
            var uri = $(this).attr("href");
             console.log(uri);
            article_list_ajax_load(uri);

            if(history.pushState){
              var state = {
                url: uri, title: document.title, type: "article_list"
              }
              history.pushState(state, document.title, uri);
            }
          });
          $('#m-next').click(function(event){
            event.preventDefault();
            var uri = $(this).attr("href");
            console.log(uri);
            article_list_ajax_load(uri);

            if(history.pushState){
              var state = {
                url: uri, title: document.title, type: "article_list"
              }
              history.pushState(state, document.title, uri);
            }
          });
        }
        gotoTop();
        bind_article_ajax();
        bind_article_list_ajax();
        bind_pager_ajax();
      }
    );
    function gotoTop(min_height){
      $("#go-top").click(function() {
        $('html,body').animate({scrollTop:0},700);
      });
      //获取页面的最小高度，无传入值则默认为600像素
      min_height ? min_height = min_height : min_height = 600;
      //为窗口的scroll事件绑定处理函数
      $(window).scroll(function(){
          //获取窗口的滚动条的垂直位置
          var s = $(window).scrollTop();
          //当窗口的滚动条的垂直位置大于页面的最小高度时，让返回顶部元素渐现，否则渐隐
          if( s > min_height){
              $("#go-top").fadeIn(200);  
          }else{
              $("#go-top").fadeOut(100);
          };
      });
    }