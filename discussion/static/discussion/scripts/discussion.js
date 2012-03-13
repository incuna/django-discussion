$(function() {
    // Forum enhancements
    // Requires jquery.form.js, jquery.autogrow.js and jquery.placeholder.js
    // 
    function init(context) {

      var allPostTextarea = $('.post-form textarea,', context);
      var allCommentTextarea = $('.comment-form textarea,', context);

      // Initialise post fields
      if ($.fn.autogrow) {
        // The class sets the height differently if we are using autogrow, otherwise uses a larger height
        allPostTextarea.addClass('autogrow').autogrow()
        allCommentTextarea.addClass('autogrow').autogrow()
      }

      if ($.fn.placeholder) {
        allPostTextarea.placeholder();
        allCommentTextarea.placeholder();
      }

      if ($.fn.ajaxSubmit) {
        // initialise the comment forms
        // Post comments via ajax
        $('.comment-form', context).bind('submit', function(){
            var form = $(this);
            form.find('textarea').focus();
            form.find(':submit').addClass('disabled').attr('disabled', true);
            form.ajaxSubmit({
              success: function(data, status_string, jqXHR) {
                form.closest('.comment-form-wrapper').before(data);
                form.find(':input:not(:hidden,:submit)').val('').blur();
                form.find('.errorlist').remove();
                form.find(':submit').removeClass('disabled').attr('disabled', false);
              },
              error: function(jqXHR, textStatus, errorThrown) {
                if (jqXHR.status == 400) {
                  var newForm = $(jqXHR.responseText);
                  form.replaceWith(newForm);
                  init(newForm.parent());
                  newForm.find('textarea').focus();
                }
              }
            });

            return false;
        })
      }

      // Scroll to the top of the textarea with a little bit of padding
      // (that is a quarter of the viewport)
      $('.post-reply', context).click(function() {
        var reply = $($(this).attr('href'));
        $('body').animate({scrollTop: reply.offset().top - $(window).height()/4 });
        reply.find('textarea').focus()
        return false;
      });

      // Load the hidden comments with ajax
      $('.post-comments .show-hidden a', context).click(function() {
        $(this).closest('.post-comments').load($(this).attr('href')+' .post-comments', '', function(responseText, textStatus, XMLHttpRequest) {
            init($(this));
            })
        return false;
      });

    }

    init();

});
