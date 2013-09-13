(function ($) {

    $(document).ready(function () {
        /**
         * Updates JD value displayed on the secondary navbar.
         */
        var updateJulianDate = function () {
            var jd = new Date().getTime() / 86400000 + 2440587.5;
            $("#current-jd").text(jd.toFixed(4));
            setTimeout(updateJulianDate, 1000);
        };
        updateJulianDate();
    });

})(jQuery);
