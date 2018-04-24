/**
 * Project: 82x
 * Author: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
 */
// Date Range Picker
(function ($) {
    var $datepicker = $('#daterangepicker');
    if ($datepicker.length > 0) {
        // Initialize the daterangepicker
        var start = moment($datepicker.data('start-date'));
        var end = moment($datepicker.data('end-date'));
        var options = {
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            opens: 'left'
        };

        function onDateSelected(start, end) {
            // Redirect on the selected date
            var url = window.location.href.split('?')[0];
            url += '?start_date=' + start.format('YYYY-MM-DD') + '&end_date=' + end.format('YYYY-MM-DD')
            window.location.href = url;
        }

        $datepicker.daterangepicker(options, onDateSelected);
        $datepicker.text(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
})(jQuery);

// Load tweets from Ajax
(function ($) {
    var $tweet_container = $('.tweet-container');
    var pagination = '<ul class="pagination">' +
        '<li class="page-item prev disabled"><a class="page-link" href="#">Prev</a></li>' +
        '<li class="page-item next disabled"><a class="page-link" href="#">Next</a></li>' +
        '</ul>';
    var loading = '<div class="loading mt-5 text-center"><img src="/static/loading.png" alt="" /></div>';
    var error = '<p class="small text-center text-danger">Unexpected error occurred. Please refresh and try again</p>';

    $tweet_container.each(function (index, element) {
        var $container = $(element),
            $list_group = $('<div class="list-group mb-3"></div>').appendTo($container),
            $pagination = $(pagination).appendTo($container),
            $summary = $($container.data('summary'));
        params = $container.data('params');

        params.page = 1;
        params.limit = 50;
        $list_group.append(loading);

        function request() {
            $pagination.children().addClass('disabled');
            $list_group.empty();
            $list_group.append(loading);
            if ($summary.length > 0) {
                $summary.empty();
            }

            // Read tweets using Ajax
            $.get('/tweets', params, function (response) {
                $list_group.empty();
                // Setup pagination
                if (response.prev_page) {
                    $pagination.children('.prev').removeClass('disabled');
                }
                if (response.next_page) {
                    $pagination.children('.next').removeClass('disabled');
                }

                if (response.tweets.length > 0) {
                    // Fill the list group
                    response.tweets.forEach(function (tweet) {
                        var created = moment(tweet.created_at);
                        var template = '<div class="list-group-item flex-column align-items-start mb-3">' +
                            '<div class="d-flex w-100 justify-content-between">' +
                            '<h5 class="mb-1">' + tweet.user.name + '</h5>\n' +
                            '<small>' + created.format('MMM Do') + '</small>' +
                            '</div>' +
                            '<p class="mb-1">' + tweet.text + '</p></div>';
                        $list_group.append(template);
                    });
                    if ($summary.length > 0) {
                        response.summary.forEach(function (sentence) {
                            $summary.append('<li>' + sentence + '</li>');
                        })
                    }
                }
            }).fail(function () {
                $list_group.html(error);
            });
        }

        // Set container height
        function container_height() {
            var window_hight = window.innerHeight;
            $list_group.height(window.innerHeight - $list_group.offset().top - 80);
            $list_group.css('overflow', 'auto');
        }

        // Handle pagination click
        $pagination.find('.page-link').on('click', function (e) {
            e.preventDefault();
            var $parent = $(this).parent();
            if ($parent.hasClass('disabled')) {
                return;
            }
            if ($parent.hasClass('prev')) {
                params.page -= 1;
            }
            if ($parent.hasClass('next')) {
                params.page += 1;
            }
            request();
        });

        container_height();
        request();
    });
})(jQuery);