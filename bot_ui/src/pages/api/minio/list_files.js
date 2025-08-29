import * as Minio from 'minio'

const minioClient = new Minio.Client({
    endPoint: "minio",
    port: 9000,
    useSSL: false,
    accessKey: "DefaultUser",
    secretKey: "DefaultPassword"
});
export default async function handler(req, res) {
    if (req.method === 'GET') {
        try {
            const { bucket } = req.query;
            const stream = minioClient.listObjects(bucket, '', true);
            const files = [];
            stream.on('data', obj => files.push(obj));
            stream.on('end', () => res.status(200).json(files));
            stream.on('error', err => res.status(500).json({ error: err.message }));
        } catch (error) {
            res.status(500).json({ error: 'Internal server error', details: error });
        }
    } else {
        res.status(405).json({ error: 'Method Not Allowed' });
    }
}