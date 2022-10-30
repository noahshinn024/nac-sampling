all: clean
	cargo build --release && cp ./target/release/nac-sampling ./out

clean:
	rm -f ./out; \
