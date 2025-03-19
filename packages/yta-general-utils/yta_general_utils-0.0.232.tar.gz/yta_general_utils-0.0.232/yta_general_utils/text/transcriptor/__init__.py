from yta_general_utils.web.scraper.chrome_scraper import ChromeScraper
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.text.transcriptor.web import TRANSCRIBER_HTML_ABSPATH, download_web_file
from typing import Union

import time


class WebRealTimeAudioTranscriptor:
    """
    Class to wrap a functionality related to real
    time audio transcription by using a web scraper.

    This class uses local files to create a simple
    web page that uses the chrome speech recognition
    to get the transcription.
    """

    _LOCAL_URL: str = f'file:///{TRANSCRIBER_HTML_ABSPATH}'
    _REMOTE_URL: str = 'https://iridescent-pie-f24ff0.netlify.app/'
    """
    The url to our local web page file.
    """
    max_time_to_wait: Union[float, None]
    """
    The maximum time the software will be waiting
    to detect an audio transcription before exiting
    with an empty result.
    """
    time_to_stop: float
    """
    The time that has to be spent once a final
    transcription has been found to consider it
    as a definitive one. There can be more final
    transcriptions after that one due to some 
    logic that I still don't understand properly.
    """
    do_use_local_web_page: bool
    """
    Flag that indicates if the resource must be a
    local web page (that will be loaded from a file
    in our system) or from a remote url.
    """

    def __init__(
        self,
        max_time_to_wait: Union[float, None] = 15.0,
        time_to_stop: float = 1.5,
        do_use_local_web_page: bool = True
    ):
        ParameterValidator.validate_positive_float('max_time_to_wait', max_time_to_wait, do_include_zero = True)
        ParameterValidator.validate_mandatory_float('time_to_stop', time_to_stop)
        ParameterValidator.validate_positive_float('time_to_stop', time_to_stop, do_include_zero = False)

        self.scraper = ChromeScraper()
        self.max_time_to_wait = (
            9999 # TODO: This is risky if no microphone or something
            if (
                max_time_to_wait == 0 or
                max_time_to_wait is None
            ) else
            max_time_to_wait
        )
        self.time_to_stop = time_to_stop
        self.do_use_local_web_page = do_use_local_web_page

        if self.do_use_local_web_page:
            # We need to make sure the file exist
            download_web_file()

        self._load()

    @property
    def url(
        self
    ) -> str:
        """
        The url that must be used to interact with the
        web page that is able to catch the audio and
        transcribe it.
        """
        return (
            self._LOCAL_URL
            if self.do_use_local_web_page else
            self._REMOTE_URL
        )

    def _load(
        self
    ):
        """
        Navigates to the web page when not yet on it.

        For internal use only.
        """
        if self.scraper.current_url != self.url:
            self.scraper.go_to_web_and_wait_until_loaded(self.url)

    def _get_transcription(
        self
    ) -> str:
        """
        Get the text that has been transcripted from the
        audio.

        For internal use only.
        """
        self._load()

        return self.scraper.find_element_by_id('final_transcription').text
    
    def _get_temp_transcription(
        self
    ) -> str:
        """
        Get the text that has been temporary transcripted 
        from the audio but is not still definitive.

        For internal use only.
        """
        self._load()

        return self.scraper.find_element_by_id('temp_transcription').text

    def _get_number_of_results(
        self
    ) -> int:
        """
        Get the amount of results that have been detected
        until the moment in which it is requested. This
        count is needed to check if the user is still
        talking or not.
        """
        self._load()

        return int(self.scraper.find_element_by_id('number_of_results').text)
    
    def _click_transcription_button(
        self
    ):
        """
        Performa click on the button that enables (or
        disables) the microphone so it starts (or ends)
        transcribing the text.

        For internal use only.
        """
        self._load()

        self.scraper.find_element_by_id('toggle').click()
    
    def transcribe(
        self
    ) -> str:
        """
        A web scraper instance loads the internal web
        that uses the Chrome speech recognition to get
        the audio transcription, by pressing the
        button, waiting for audio input through the
        microphone, and pressing the button again.

        If the page was previously loaded it won't be
        loaded again.
        """
        self._load()

        WAITING_TIME = 0.1

        self._click_transcription_button()

        time_elapsed = 0
        final_transcription_time_elapsed = 0
        transcription = ''
        number_of_results = 0
        while (
            time_elapsed < self.max_time_to_wait and
            (
                (
                    final_transcription_time_elapsed != 0 and
                    (final_transcription_time_elapsed + self.time_to_stop) > time_elapsed
                ) or
                final_transcription_time_elapsed == 0
            )
        ):
            tmp_final_transcription = self._get_transcription()
            tmp_number_of_results = self._get_number_of_results()
            """
            If temporary transcription is changing,
            we are still getting audio transcripted
            so we need to keep waiting for the 
            final transcription. We are indicating
            the amount of words detected, so if that
            number keeps increasing, we need to keep
            waiting
            """
            if (
                tmp_number_of_results > number_of_results or
                tmp_final_transcription != transcription
            ):
                # If final transcription has changed or the
                # amount of events keeps increasing, we 
                # keep waiting
                final_transcription_time_elapsed = time_elapsed

                if tmp_number_of_results > number_of_results:
                    number_of_results = tmp_number_of_results

                if tmp_final_transcription != transcription:
                    transcription = tmp_final_transcription
                
            time.sleep(WAITING_TIME)
            time_elapsed += WAITING_TIME

        self._click_transcription_button()

        return transcription



