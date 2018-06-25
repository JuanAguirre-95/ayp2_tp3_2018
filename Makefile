nombre_tp = tp3

sources = grafo.py

extras = Makefile
 
git_add:
	git add $(sources) $(extras)
git_commit: git_add
	@read -p "Mensaje del commit: " MENSAJE; \
    git commit -m "$$MENSAJE"
	
git_pull:
	git pull origin
	
git_push:
	git push origin master
	
run: $(sources)
	python3 grafo.py
	 
	
.PHONY : clean	
clean:
	-rm analog

zip:
	zip $(nombre_tp).zip $(sources) $(extras) 
