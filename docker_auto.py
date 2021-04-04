- hosts: web
  vars_prompt:
      - name: "port"
        prompt: "which port you want to expose: "
        private: no
  tasks:
  - name: "creating the mounting point for cdrom"
    file:
        path: /dvd
        state: directory
  - name: "configuring yum for docker"  
    yum_repository:
      name: "docker"
      description: "docker repo"
      baseurl: " https://download.docker.com/linux/centos/7/x86_64/stable/ "
      gpgcheck: no 
  - name: "making directory"
    file:
        path: /root/webpage/
        state: directory
  - name: "copying webpage"
    copy:
        dest: /root/webpage/
        src: /var/www/html/web.html
  - name: "installing docker"
    command: dnf install docker-ce --nobest -y
  - name: starting the service 
    service:
        name: docker
        state: started
  - name: "completing the dependency"
    pip:
        name: docker
  - name: "pulling and starting container httpd"      
    docker_container:
        name: "container"
        image: httpd
        state: started
        ports: 
           - "{{ port }}:80"
        volumes: 
            - /root/webpage/:/usr/local/apache2/htdocs
  - name: "allowing exposing port"
    firewalld:
        port: "{{ port }}/tcp"
        permanent: yes
        immediate: yes
        state: enabled
    
