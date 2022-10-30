all: clean
	cargo build --release && cp ./target/release/nac-sampling ./

clean:
	rm -f ./out; \
