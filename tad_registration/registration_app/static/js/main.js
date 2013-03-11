$(function() {
    var addParticipant = function() {
        $('.participants').append($('.participant:first').clone()); 
    },
        updateParticipantCount = function() {
            participants = $('.participant');
            _.each(participants, function(el, i) {
                $el = $(el);
                inputs = $el.find('input, select, textarea');
                inputs.attr('data-index', i);
            });
        },
        appendIndexesToNames = function() {
            _.each($('input, select, textarea'), function(el) {
                $el = $(el);
                index = $el.attr('data-index');
                if($el.attr("type") !== 'hidden' && index !== undefined) {
                    name = $el.attr('name');
                    $el.attr('name', name + "-" + index);
                }
            });
        };

    $(".add-participant").click(function(e) {
        addParticipant();
        updateParticipantCount();
    });

    $("#registration-form").submit(function(e) {
        appendIndexesToNames();
        return true;
    });


    updateParticipantCount();
});

