const ytdl = require('ytdl-core');
const axios = require('axios');

exports.name = '/youtube/video';

exports.index = async (req, res, next) => {
    const url = req.query.url;

    if (!url) {
        return res.status(400).json({ error: 'Missing URL parameter' });
    }

    try {
        // Kiểm tra xem URL có hợp lệ không
        if (!ytdl.validateURL(url)) {
            return res.status(400).json({ error: 'Invalid YouTube URL' });
        }

        const videoInfo = await ytdl.getInfo(url);

        const title = videoInfo.videoDetails.title;
        const description = videoInfo.videoDetails.description;
        const thumbnail = videoInfo.videoDetails.thumbnails[0].url;

        const formats = ytdl.filterFormats(videoInfo.formats, 'videoandaudio');
        const highestQualityFormat = formats[0];

        const audioFormats = ytdl.filterFormats(videoInfo.formats, 'audioonly');
        const highestQualityAudio = audioFormats[0];

        // Kiểm tra xem có định dạng video và audio không
        if (!highestQualityFormat || !highestQualityAudio) {
            return res.status(404).json({ error: 'No suitable video or audio format found' });
        }

        res.json({
            title: title,
            description: description,
            thumbnail: thumbnail,
            video: {
                url: highestQualityFormat.url,
                quality: highestQualityFormat.qualityLabel,
                format: highestQualityFormat.container
            },
            audio: {
                url: highestQualityAudio.url,
                quality: highestQualityAudio.audioQuality,
                format: highestQualityAudio.container
            }
        });
    } catch (error) {
        console.error('Error:', error);

        if (error.message.includes('Video unavailable')) {
            return res.status(404).json({ error: 'This video is unavailable. It may have been removed or is not accessible in your region.' });
        } else if (error.message.includes('Video is private')) {
            return res.status(403).json({ error: 'This video is private and cannot be accessed.' });
        } else if (error.message.includes('Video is age-restricted')) {
            return res.status(403).json({ error: 'This video is age-restricted and cannot be accessed without authentication.' });
        }

        res.status(500).json({ error: 'An error occurred while processing the request', details: error.message });
    }
};