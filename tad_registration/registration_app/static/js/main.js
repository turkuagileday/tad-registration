$(function() {
    var addParticipant = function() {
        participant = $('.participant:first').clone();
        participant.find("input[type=text]").val("");
        participant.find("input[type=checkbox]").attr("checked", false);
        $('.participants').append(participant);
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
        },
        showSelectedBillingType = function() {
            selected_type = $("#id_billing_type option:selected").val();
            if (selected_type === "email") {
                $(".normal_type").show();
                $(".post_type, .e_type").hide();
            } else if (selected_type === "post") {
                $(".post_type").show();
                $(".normal_type, .e_type").hide();
            } else if (selected_type === "ebilling") {
                $(".e_type").show();
                $(".normal_type, .post_type").hide();
            } else {
                $(".normal_type, .post_type, .e_type").hide();
            }
        },
        clearAllButSelected = function() {
            selected_type = $("#id_billing_type option:selected").val();
            if (selected_type === "email") {
                $(".post_type, .e_type").html("");
            } else if (selected_type === "post") {
                $(".normal_type, .e_type").html("");
            } else if (selected_type === "ebilling") {
                $(".e_type").show();
                $(".normal_type, .post_type").html("");
            }
        },
        removeParsleyValidationFromInvisibleElements = function() {
          $('#registration-form').parsley('addListener', {
            onFieldValidate: function(el) {
              if (!$(el).is(':visible')) {
                return true;
              }
              return false;
            }
          });
        };

    $("#id_billing_type").change(showSelectedBillingType);
    $("#add-participant").on('click', function(e) {
        e.preventDefault();
        addParticipant();
        updateParticipantCount();
    });

    $("#registration-form").submit(function(e) {
        appendIndexesToNames();
        clearAllButSelected();
        removeParsleyValidationFromInvisibleElements();
        $("#participant-count").attr("value", $(".participant").length)
        return true;
    });


    updateParticipantCount();
    showSelectedBillingType();
});

