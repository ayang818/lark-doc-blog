docker build -t "lard_doc_blog_py:1.0" .
echo 'suc build'
docker rm -fv "open_lark_doc_blog_be"
echo "suc delete"
docker run -d --name "open_lark_doc_blog_be" -p 5000:80 lard_doc_blog_py:1.0
echo 'suc run'