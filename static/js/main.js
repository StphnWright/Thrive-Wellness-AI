$(document).ready(function() {
    function handleFormSubmit(formId, url) {
        $(formId).submit(function(e) {
            e.preventDefault();
            const formData = $(this).serialize();
            $.ajax({
                type: "POST",
                url: url,
                data: formData,
                success: function(response) {
                    console.log("Response received:", response);
                    const formattedResponse = response.response.replace(/\n/g, '<br>');
                    $(formId + '-response').html('<p>' + formattedResponse + '</p>');
                    $(formId + '-response').next('.reset-section').show();
                },
                error: function(error) {
                    console.log("Error:", error);
                    $(formId + '-response').html('<p>An error occurred. Please try again.</p>');
                }
            });
        });
    }

    handleFormSubmit('#fitness-form', '/fitness');
    handleFormSubmit('#nutrition-form', '/nutrition');
    handleFormSubmit('#mental-health-form', '/mental_health');

    $('.reset-btn').click(function() {
        const section = $(this).closest('.col-md-4');
        section.find('form')[0].reset();
        section.find('.form-response').empty();
        section.find('.reset-section').hide();
    });
});
