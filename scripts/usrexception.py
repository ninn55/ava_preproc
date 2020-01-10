

class UsrError(Exception):
    """
    Base class
    """
    pass

class FileNOTFound(UsrError):
    """
    Try to read a file that not exist
    """
    pass

class GenFailed(UsrError):
    """
    Failed to generate keyfrmaes or clips use ffmpeg somehow
    """
    pass

class ExcessVideoDuration(UsrError):
    """
    Trying to generate keyframe or video out side video duration
    Default behavier. Discard said frames and clips.
    """
    pass

class InnerLogicError(UsrError):
    """
    This exception is raised when some inner logic error is detected
    """
    pass

class ShellError(UsrError):
    """
    Shell
    """
    pass