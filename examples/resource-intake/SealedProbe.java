public class SealedProbe {
    public static void main(String[] args) throws Exception {
        Class<?> shape = Class.forName("Shapes$Shape");
        Class<?>[] permitted = shape.getPermittedSubclasses();
        System.out.println(shape.isSealed() + ":" + (permitted == null ? 0 : permitted.length));
    }
}
