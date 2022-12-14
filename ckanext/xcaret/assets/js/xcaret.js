this.ckan.module('xcaret-form', function ($) {
  return {
    initialize: function () {
      var message = this._('There are unsaved modifications to this form');

      $.proxyAll(this, /_on/);

      this.el.incompleteFormWarning(message);

      // Disable the submit button on form submit, to prevent multiple
      // consecutive form submissions.
      this.el.on('submit', this._onSubmit);
    },
    _onSubmit: function () {

      // The button is not disabled immediately so that its value can be sent
      // the first time the form is submitted, because the "save" field is
      // used in the backend.
      setTimeout(function() {
        this.el.find('button[name="save"]').attr('disabled', true);
      }.bind(this), 0);
    }
  };
});


$("#field-homepage-style").change(function() {
    if ($(this).val() == "4") {
      $('#xcaret-options').show();
    } else {
      $('#xcaret-options').hide();
    }
  });

  $(document).ready(function () {     
    var style = $("#field-homepage-style").val();

    if (style == "4") {
      $('#xcaret-options').show();
    } else {
      $('#xcaret-options').hide();
    }
  });